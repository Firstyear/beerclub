from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, Drink, Beer, Payment, BeerInst, Stock
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Reconciles Account details from payments and drinks. Creates accounts for all Users'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for beerinst in BeerInst.objects.all():
            beerinst.reconcile_stock()
            if beerinst.stock_total < 0:
                # Create a dummy StockImport, and StockMoved
                si = Stock(beerinst=beerinst, quantity=beerinst.stock_total * -1, comment="Auto created by negative_stock_fix")
                # To neutralise these numbers.
                si.save()
                print(beerinst)
                print(si)
            beerinst.save()
