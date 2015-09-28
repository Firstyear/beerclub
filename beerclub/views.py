import json

from datetime import date, timedelta

from django.http import HttpResponseForbidden
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from django.db import models

from beerclub.models import Account, Beer, Drink, Payment, BeerInst, Stock, ClubAccount
from beerclub.forms import DrinkForm, AccountCreateForm, StockCreateForm
# Create your views here.

class RootView(TemplateView):
    template_name = 'beerclub/root.html'

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(RootView, self).dispatch(*args, **kwargs)


class AccountListView(ListView):
    model = Account
    template_name = 'beerclub/account_list.html'

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects.all()

    def get_queryset(self):
        if self.request.GET.has_key('search') and self.request.user.is_staff:
            search = self.request.GET['search']
            return self.model.objects.filter( Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) )
        elif self.request.user.is_staff:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=self.request.user)

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AccountListView, self).dispatch(*args, **kwargs)

class LegendsListView(ListView):
    model = Account
    template_name = 'beerclub/legends_list.html'

    def get_queryset(self):
        if not self.request.user.is_staff:
            return HttpResponseForbidden()
            #return self.model.objects.filter(user=self.request.user)
        return self.model.objects.all()

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    #def dispatch(self, *args, **kwargs):
    #    return super(LegendsListView, self).dispatch(*args, **kwargs)

class BeerListView(ListView):
    model = BeerInst
    template_name = 'beerclub/beer_list.html'

    def get_queryset(self):
        if self.request.GET.has_key('search'):
            search = self.request.GET['search']
            try:
                beerinst_pk = int(self.request.GET['beer_pk'])
            except:
                beerinst_pk = 0
            return self.model.objects.filter(Q(beer__name__icontains=search) | Q(beer__brewery__name__icontains=search) | Q(barcode=search) | Q(barcode_pack=search) | Q(pk=beerinst_pk))
        else:
            #return self.model.objects.all()
            return None

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    #def dispatch(self, *args, **kwargs):
    #    return super(BeerListView, self).dispatch(*args, **kwargs)

class BeerUniqueListView(ListView):
    model = BeerInst
    template_name = 'beerclub/beer_list.html'

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        spec_drinks = account.drink_set.filter(date__year=date.today().year).values_list('beerinst__beer__id', flat=True).distinct()
        available_beers = BeerInst.objects.filter(stock_total__gt=0)
        available = filter(lambda x: x.beer.id not in spec_drinks, available_beers)
        return sorted(available, cmp=lambda a,b: a.beer.name < b.beer.name)

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    #def dispatch(self, *args, **kwargs):
    #    return super(BeerUniqueListView, self).dispatch(*args, **kwargs)

class DrinkCreateView(FormView):
    template_name = 'beerclub/drink_create.html'
    form_class = DrinkForm
    success_url = "/bc/drink/create/"

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(DrinkCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        account_id = data.get('name_pk', 0)
        account = Account.objects.get(pk=account_id)
        beer_id = data.get('beer_pk', 0)
        payee_id = data.get('payee_name_pk', 0)
        value = data.get('value', 0)
        if value == 0:
            #### Do nothing
            pass
        elif value < 0:
            messages.error(self.request, "Cannot add negative payment")
        else:
            payment = Payment(account=account, value=value, date=date.today())
            payment.clean()
            payment.save()
            messages.success(self.request, 'Payment added! %s' % payment)
        ### Drink sales
        try:
            if beer_id != 0:
                beerinst = BeerInst.objects.get(pk=beer_id)
                drink = create_drink_sale(account, beerinst, data['free'], data['special'], payee_id=payee_id)
                messages.success(self.request, 'Drink added! %s' % drink)
        except Exception as e:
            messages.error(self.request, e)
        return super(DrinkCreateView, self).form_valid(form)

class AccountCreateView(FormView):
    template_name = 'beerclub/account_create.html'
    form_class = AccountCreateForm
    success_url = "/bc/accounts"

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(AccountCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        name = data.get('name', None)
        #barcode = data.get('barcode', None)
        if name is not None:
            user = None
            try:
                user = User.objects.get(username=name)
            except:
                ldapobj = LDAPBackend()
                user = ldapobj.populate_user(name)
                if user is not None and not user.is_anonymous():
                    print("%s -> True" % name)
                else:
                    print("%s -> False" % name)
                user.save()
            account = None
            try:
                account = Account.objects.get(user=user)
            except:
                account = Account(user=user, balance=0)
            print("Creating %s" % user)
            #account.barcode = barcode
            account.save()
            messages.success(self.request, "Added %s" % user)
        return super(AccountCreateView, self).form_valid(form)

class StockView(FormView):
    template_name = 'beerclub/stock_create.html'
    form_class = StockCreateForm
    success_url = '/bc/stock/import/'

    def stock_import(self, beerinst, quantity):
        si = Stock(beerinst=beerinst, quantity=quantity)
        si.clean()
        si.save()
        messages.success(self.request, 'Beer added %s : %s' % (beerinst, quantity))

    #@method_decorator(permission_required('beerclub.can_login', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(StockView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        barcode = data.get('barcode', None)
        beerinst_pack = BeerInst.objects.filter(barcode_pack=barcode).first()
        beerinst_sing = BeerInst.objects.filter(barcode=barcode).first()
        if beerinst_pack is not None:
            self.stock_import(beerinst_pack, beerinst_pack.quantity_pack)
        elif beerinst_sing is not None:
            self.stock_import(beerinst_sing, 1)
        else:
            print('NO SUCH BEER')
            messages.error(self.request, 'No such barcode')
        return super(StockView, self).form_valid(form)

class StatsView(TemplateView):
    template_name = 'beerclub/stats.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return super(StatsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        year_drinks = Drink.objects.filter(date__year=date.today().year)
        accounts = Account.objects.all()
        total_volume = Drink.objects.filter(date__year=date.today().year).aggregate(beerinst__volume=models.Sum('beerinst__volume'))['beerinst__volume']
        if total_volume is None:
            total_volume = 0
        ### Total volume
        total_ethanol = 0
        for drink in year_drinks:
            #total_volume += drink.beerinst.volume
            total_ethanol += drink.beerinst.volume_ethanol
        caccounts = ClubAccount.objects.all()
        caccount = None
        if len(caccounts) == 0:
            caccount = ClubAccount()
        else:
            caccount = caccounts[0]
        caccount.reconcile()
        context['caccount'] = caccount

        context['total_volume'] = total_volume / 1000.0
        context['total_ethanol'] = total_ethanol / 1000.0
        context['std_drinks'] = total_ethanol / 12.67

        context['top_five'] = sorted(accounts, key=lambda account: account.drinks_unique_had, reverse=True)[:5]
        #context['most_volume'] = sorted(accounts, key=lambda account: account.drinks_volume, reverse=True)[0]
        #context['most_volume_ethanol'] = sorted(accounts, key=lambda account: account.drinks_ethanol_volume, reverse=True)[0]
        return context

##########################################

def create_drink_sale(account, beerinst, free, special, selfserve=False, payee_id=0):
    drink = Drink(date=date.today(), account=account, beerinst=beerinst, selfserve=selfserve)
    if free == True:
        drink.debt = 0
    if payee_id == 0:
        drink.payee = account
    else:
        drink.payee = Account.objects.get(id=payee_id)
    #if special == True:
    #    drink.special = True
    # Because we now hand this via the JS, we can better use this
    drink.special = special
    drink.clean()
    if account.special_due < 1 and special is True:
        raise Exception("You are not yet due a special")
    drink.save()
    return drink


