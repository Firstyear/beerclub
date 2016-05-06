from django.core.management.base import BaseCommand, CommandError
from beerclub.models import Account, Drink, Beer, Payment, BeerInst, Stock
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Merges two beers into each other, but leaves all BeerInsts attached.'

    def add_arguments(self, parser):
        parser.add_argument('beer_inst_id', nargs='+', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        ids = map(lambda x: int(x), options['beer_inst_id'])
        beer_keep = BeerInst.objects.get(id=ids.pop(0))
        others = map(lambda x: BeerInst.objects.get(id=x), ids)
        print("About to merge the following:")
        for b in others: print(" * %s " % b)
        print("Into beer instance '%s'" % beer_keep)
        if raw_input("ARE YOU SURE? TYPE 'YES' # ") == "YES":
            print("Doing the thing")
            for b in others:
                for s in Stock.objects.filter(beerinst=b):
                    print(s)
                    s.beerinst = beer_keep
                    s.save()
                for d in Drink.objects.filter(beerinst=b):
                    print(d)
                    d.beerinst = beer_keep
                    d.save()
                b.delete()
            print('RECOGNITION FOR DOING THE THING')
