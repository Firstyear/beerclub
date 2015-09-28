from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, Drink, Beer, Payment, BeerInst, StockImport, StockMove
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Reconciles Account details from payments and drinks. Creates accounts for all Users'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for beerinst in BeerInst.objects.all():
            beerinst.reconcile_stock()
            if beerinst.stock_fridge < 0 and beerinst.stock_total < 0:
                # Create a dummy StockImport, and StockMoved
                si = StockImport(beerinst=beerinst, quantity=beerinst.stock_total * -1, comment="Auto created by migrationfixup")
                sm = StockMove(beerinst=beerinst, quantity=beerinst.stock_total * -1, comment="Auto created by migrationfixup")
                # To neutralise these numbers.
                si.save()
                sm.save()
            beerinst.save()

        ### We want to find the most unique beers this year.
        ### We want to find the most volume consumed
        ### Most volume of Alcohol consumed.
        ### Most "same" beer drunk.
