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
            if account.balance < 0 and account.active:
                self.stdout.write("User in debt")
                message_body = """Greetings {firstname},

That time has come, where the debts must be paid: And a beerclub member always
pays his debts.

You owe the sum of ${debt}

Please contact your nearest Beerclub representative to settle the matter,

--
Sincerely,

The BeerMeisters
""".format(firstname=account.user.first_name, debt=(account.balance_dollars * -1.0))
                message = ('Beerclub notification {date}'.format(date=date.today()),
                            message_body,
                            'noreply@adelaide.edu.au',
                            [account.user.email])
                messages += (message,)
            elif not account.active:
                self.stdout.write("User in debt, but inactive")
            else:
                self.stdout.write("User not in debt")
        if len(messages) > 0:
            for message in messages:
                print(message)
            send_mass_mail(messages, fail_silently=False)
            #print(messages)

