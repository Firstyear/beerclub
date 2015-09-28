from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, Drink, Beer, Payment
from django.contrib.auth.models import User
from django.db import transaction
from django.core.mail import send_mass_mail
from datetime import date

class Command(BaseCommand):
    args = ''
    help = 'Will send out emails notifying people of their debts. A beer club member always pays his debts'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Reconcile accounts first.
        messages = ()
        accounts = Account.objects.all()
        for account in accounts:
            self.stdout.write("Reconciling %s ... " % account, ending='')
            #We have an account.
            account.reconcile()
            account.save()
            self.stdout.write("$ %s / due %s" % (account.balance_dollars, account.special_due))
            message_body = ""
            if account.balance < 0:
                self.stdout.write("User in debt")
                message_body = """Greetings {firstname},

That time has come, where we the BeerMeisters throw a celebration to reward our
loyal members. We are conducting a free drinks evening in the ITS cafe beginning
at 5pm Friday 14th of November. To participat you must have a balance of $0 or
higher.

Your current balance is ${debt}. Please contact William to settle this.

--
Sincerely,

The BeerMeisters
""".format(firstname=account.user.first_name, debt=(account.balance_dollars))
            else:
                self.stdout.write("User not in debt")
                message_body = """Greetings {firstname},


That time has come, where we the BeerMeisters throw a celebration to reward our
loyal members. We are conducting a free drinks evening in the ITS cafe beginning
at 5pm Friday 14th of November. To participat you must have a balance of $0 or
higher.

Your current balance is ${debt}. You can enjoy a warm fuzzy feeling, and a free
drink with your fellows!

--
Sincerely,

The BeerMeisters
""".format(firstname=account.user.first_name, debt=(account.balance_dollars))

            message = ('Beerclub notification {date}'.format(date=date.today()),
                        message_body,
                        'noreply@adelaide.edu.au',
                        [account.user.email])
            messages += (message,)
        if len(messages) > 0:
            for message in messages:
                print(message)
            #send_mass_mail(messages, fail_silently=False)
            print(messages)

