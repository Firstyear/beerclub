from django.core.management.base import BaseCommand, CommandError
from beerclub.models import Account, Drink, Brewery, Beer
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Merges two breweries into each other, but leaves all BeerInsts attached.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ids = map(lambda x: int(x), args)
        brewery_keep = Brewery.objects.get(id=ids.pop(0))
        others = map(lambda x: Brewery.objects.get(id=x), ids)
        print("About to merge the following:")
        for b in others: print(" * %s " % b)
        print("Into brewery '%s'" % brewery_keep)
        if raw_input("ARE YOU SURE? TYPE 'YES' # ") == "YES":
            print("Doing the thing")
            for b in others:
                for bi in Beer.objects.filter(brewery=b):
                    print(bi)
                    bi.brewery = brewery_keep
                    bi.save()
                b.delete()
            print('RECOGNITION FOR DOING THE THING')
