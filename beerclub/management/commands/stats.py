from django.db import models
from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, Drink, Beer, Payment
from django.contrib.auth.models import User
from django.db import transaction
from datetime import date, timedelta

class Command(BaseCommand):
    args = ''
    help = 'Reconciles Account details from payments and drinks. Creates accounts for all Users'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        year_drinks = Drink.objects.filter(date__year=date.today().year)
        accounts = Account.objects.all()
        total_volume = Drink.objects.filter(date__year=date.today().year).aggregate(beerinst__volume=models.Sum('beerinst__volume'))['beerinst__volume']
        ### Total volume
        total_ethanol = 0
        for drink in year_drinks:
            #total_volume += drink.beerinst.volume
            total_ethanol += drink.beerinst.volume_ethanol
        std_drinks = total_ethanol / 12.67

        top_five = sorted(accounts, key=lambda account: account.drinks_unique_had, reverse=True)[:5]
        most_volume = sorted(accounts, key=lambda account: account.drinks_volume, reverse=True)[0]
        most_volume_ethanol = sorted(accounts, key=lambda account: account.drinks_ethanol_volume, reverse=True)[0]

        print("Total Volume of Beer: %sL" % (total_volume / 1000.0))
        print("Total Volume of Ethanol: %sL" % (total_ethanol / 1000.0))
        print("Total Standard Drinks: %s" % std_drinks)
        print("Most Volume of Beer: %sL %s %s" % (most_volume.drinks_volume / 1000.0 , most_volume.user.first_name, most_volume.user.last_name))
        print("Most Volume of Ethanol: %sL %s %s" % (most_volume_ethanol.drinks_ethanol_volume / 1000.0 , most_volume_ethanol.user.first_name, most_volume_ethanol.user.last_name))

        print("Top 5:")
        for account in top_five:
            print("%s : %s %s" % (account.drinks_unique_had, account.user.first_name, account.user.last_name) )

