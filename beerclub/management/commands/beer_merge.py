from django.core.management.base import BaseCommand, CommandError
from beerclub.models import Account, Drink, Beer, Payment, BeerInst, Stock
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Merges two beers into each other, but leaves all BeerInsts attached.'

    def add_arguments(self, parser):
        parser.add_argument('beer_id', nargs='+', type=int)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ids = map(lambda x: int(x), options['beer_id'])
        beer_keep = Beer.objects.get(id=ids.pop(0))
        others = map(lambda x: Beer.objects.get(id=x), ids)
        print("About to merge the following:")
        for b in others: print(" * %s " % b)
        print("Into beer '%s'" % beer_keep)
        if raw_input("ARE YOU SURE? TYPE 'YES' # ") == "YES":
            print("Doing the thing")
            for b in others:
                for bi in BeerInst.objects.filter(beer=b):
                    print(bi)
                    bi.beer = beer_keep
                    bi.save()
                b.delete()
            print('RECOGNITION FOR DOING THE THING')
