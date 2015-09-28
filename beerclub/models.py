from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils import timezone

class Brewery(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Beer(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    brewery = models.ForeignKey(Brewery)
    abvp = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('beerclub:beer_update', kwargs={'pk' : self.id})

class BeerInst(models.Model):
    beer = models.ForeignKey(Beer)
    container = models.CharField(max_length=8, choices=(
        ('can', 'can'),
        ('bottle' , 'bottle'),
        ('horn' , 'horn'),
        ('glass' , 'glass'),
        ), help_text="Packaging the beer comes in."
    )
    volume = models.IntegerField()
    unit_sale_price = models.IntegerField(help_text="This is a value in AU cents", default=400)
    #cost_price = models.IntegerField(help_text="This is a value in AU cents")
    special = models.BooleanField(default=False)
    barcode = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True, default=None)
    barcode_pack = models.CharField(max_length=50, null=True, blank=True, db_index=True, default=None)
    quantity_pack = models.PositiveIntegerField(null=True, blank=True, default=6)
    stock_total = models.IntegerField(default=0)
    stock_value = models.IntegerField(default=0)

    class Meta:
        ordering = ["beer__name"]

    def __unicode__(self):
        return '%s, %s (%s) %sml' % (self.beer.name, self.beer.brewery.name, 
            self.container, self.volume)

    def drink_set_year(self):
        return self.drink_set.filter(date__year=date.today().year)

    def get_absolute_url(self):
        return reverse('beerclub:beerinst_update', kwargs={'pk' : self.id})

    @property
    def volume_ethanol(self):
        return self.volume * (self.beer.abvp / 100.0)

    def reconcile_stock(self):
        total_imported = self.stock_set.all().aggregate(quantity=models.Sum('quantity'))['quantity']
        total_writeoff = self.stockwriteoff_set.all().aggregate(quantity=models.Sum('quantity'))['quantity']
        if total_imported is None:
            total_imported = 0
        if total_writeoff is None:
            total_writeoff = 0
        total_sold = self.drink_set.count()
        self.stock_total = total_imported - (total_sold + total_writeoff)
        self.stock_value = self.stock_total * self.unit_sale_price
        #print(self.stock_total)
        self.save()

    def clean(self):
        if self.barcode == '':
            self.barcode = None
        if self.barcode_pack == '':
            self.barcode_pack = None

class Stock(models.Model):
    # How many beers were imported to the office at some date.
    beerinst = models.ForeignKey(BeerInst)
    quantity = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True, db_index=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return "%s %s : %s" % (self.datetime, self.beerinst, self.comment)

    class Meta:
        ordering = ["-datetime"]

class StockTake(models.Model):
    """
        This is a short lived temporal model just used to calculate the set of beers
        In stock from the ones not.
        The main reason for this is a way to do set changes and stock fix ups
    """
    beerinst = models.ForeignKey(BeerInst)
    quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s : %s" % (self.beerinst, self.quantity)

class StockWriteOff(models.Model):
    beerinst = models.ForeignKey(BeerInst)
    quantity = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True, db_index=True)
    comment = models.CharField(max_length=500)

    def __unicode__(self):
        return "%s %s : %s" % (self.datetime, self.beerinst, self.comment)

    class Meta:
        ordering = ["-datetime"]

class Account(models.Model):
    user = models.ForeignKey(User)
    balance = models.IntegerField(help_text="This is a value in AU cents. It is reconciled as a set of payments and drinks")
    #barcode = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)
    #special_due = models.IntegerField(default=0)
    class Meta:
        ordering = ["user__first_name"]
        permissions = (("can_login", "Can login"),)

    @property
    def active(self):
        year_past = date.today() - timedelta(days=366)
        num_drinks = self.drink_set.filter(date__gt=year_past).count()
        if num_drinks > 0:
            return True
        return False

    @property
    def drinks_had(self):
        spec_drinks = self.drink_set.filter(date__year=date.today().year).values_list('beerinst__beer__id', flat=True)
        return len(spec_drinks)

    @property
    def drinks_unique_had(self):
        spec_drinks = self.drink_set.filter(date__year=date.today().year).values_list('beerinst__beer__id', flat=True).distinct()
        return len(spec_drinks)

    @property
    def drinks_volume(self):
        spec_drinks = self.drink_set.filter(date__year=date.today().year).values_list('beerinst__volume', flat=True)
        return reduce(lambda x, y: x + y, spec_drinks, 0)

    @property
    def drinks_ethanol_volume(self):
        spec_drinks = self.drink_set.filter(date__year=date.today().year)
        ethanol_volumes = map(lambda drink: drink.beerinst.volume_ethanol, spec_drinks)
        return reduce(lambda x, y: x + y, ethanol_volumes, 0)

    @property
    def special_had(self):
        spec_drinks = self.drink_set.filter(special=True, date__year=date.today().year).values_list('beerinst__beer__id', flat=True)
        return len(spec_drinks)

    @property
    def special_due(self):
        # This year
        num_spec = self.drinks_unique_had / 10 # This is an implicit floor because int not float
        return num_spec - self.special_had

    @property
    def balance_dollars(self):
        return float(self.balance) / 100

    @property
    def current_drink(self):
        time_threshold = timezone.now() - timedelta(hours=1)
        return self.drink_set.filter(datetime__gt=time_threshold).order_by('-datetime').first()

    def reconcile(self):
        ### Needs to be all time, we carry debts over years.
        ###### We actually need the payee set now
        drinks = self.drink_payee_set.all().aggregate(debt=models.Sum('debt'))
        payments = self.payment_set.all().aggregate(value=models.Sum('value'))
        self.balance = (payments['value'] or 0) - (drinks['debt'] or 0)

    def clean(self):
        self.reconcile()

    def __unicode__(self):
        return "%s %s (%s)" % (self.user.first_name, self.user.last_name, self.user)

class Drink(models.Model):
    account = models.ForeignKey(Account)
    payee = models.ForeignKey(Account, related_name="drink_payee_set")
    beerinst = models.ForeignKey(BeerInst)
    special = models.BooleanField(blank=True, default=None)
    debt = models.IntegerField(blank=True,help_text="This is a value in AU cents. This value is populated automatically")
    date = models.DateField(auto_now_add=True, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    rating = models.PositiveIntegerField(null=True, default=3, blank=True)
    selfserve = models.BooleanField(default=False)

    class Meta:
        ordering = ["beerinst__beer__name"]
        get_latest_by = 'datetime'

    def clean(self):
        if self.rating > 5:
            self.rating = 5
        if self.special is None:
            self.special = self.beerinst.special
        if self.debt is None:
            if self.special is False:
                self.debt = self.beerinst.unit_sale_price
            else:
                self.debt = 0

    def __unicode__(self):
        msg = "%s -> %s" % (self.account.__unicode__(), self.beerinst.__unicode__())
        if self.special:
            msg = "%s SPECIAL" % (msg)
        if self.account != self.payee:
            msg = "%s paid for by %s" % (msg, self.payee.__unicode__())
        return msg

class Payment(models.Model):
    account = models.ForeignKey(Account)
    value = models.IntegerField(help_text="This is a value in AU cents")
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s -> +%sc" % (self.account.__unicode__(), self.value)

class ClubAccount(models.Model):
    balance = models.IntegerField()

    def reconcile(self):
        on_hand = 0
        payment = Payment.objects.all().aggregate(value=models.Sum('value'))
        expenditure = Expenditure.objects.all().aggregate(cost=models.Sum('cost'))
        self.balance = (payment['value'] or 0) - (expenditure['cost'] or 0)
        self.save()

class Expenditure(models.Model):
    cost = models.IntegerField()
    comment = models.CharField(max_length=500)
    caccount = models.ForeignKey(ClubAccount)

    def __unicode__(self):
        return self.comment

def account_auto_reconcile(sender, **kwargs):
    instance = kwargs['instance']
    instance.account.reconcile()
    instance.account.save()

post_save.connect(account_auto_reconcile, sender=Drink)
post_save.connect(account_auto_reconcile, sender=Payment)

def stock_auto_reconcile(sender, **kwargs):
    instance = kwargs['instance']
    instance.beerinst.reconcile_stock()
    # Do the thing
    pass

post_save.connect(stock_auto_reconcile, sender=Drink)
post_save.connect(stock_auto_reconcile, sender=Stock)
post_save.connect(stock_auto_reconcile, sender=StockWriteOff)



