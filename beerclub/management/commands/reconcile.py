from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, ClubAccount, BeerInst
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Reconciles Account details from payments and drinks. Creates accounts for all Users'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for beerinst in BeerInst.objects.all():
            beerinst.reconcile_stock()
            beerinst.save()
        for user in User.objects.all():
            account = Account.objects.filter(user=user)
            if len(account) == 1:
                self.stdout.write("Reconciling %s ... " % user, ending='')
                #We have an account.
                account[0].reconcile()
                account[0].save()
                self.stdout.write("$ %s / due %s" % (account[0].balance_dollars, account[0].special_due))
            else:
                self.stdout.write("Creating %s" % user)
                account = Account(user=user, balance=0)
                account.save()
        caccounts = ClubAccount.objects.all()
        caccount = None
        if len(caccounts) == 0:
            caccount = ClubAccount()
        else:
            caccount = caccounts[0]
        caccount.reconcile()
        self.stdout.write("Beerclub assets cents %s" % caccount.balance)
        beerassetvalue = 0
        beerstocks = BeerInst.objects.filter(stock_total__gt=0)
        for beer in beerstocks:
            self.stdout.write("%s %s" % (beer.__unicode__(), beer.stock_value))
            beerassetvalue += beer.stock_value
        self.stdout.write("Beerclub beer stock value %s" % beerassetvalue)


