from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Account, Drink, Beer, Payment
from django.contrib.auth.models import User
from django.db import transaction
from django_auth_ldap.backend import LDAPBackend

class Command(BaseCommand):
    args = ''
    help = 'Populates a user account from ldap via uid (Space seperated list)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if len(args) <= 0:
            return
        for arg in args:
            ldapobj = LDAPBackend()
            user = ldapobj.populate_user(arg)
            if user is not None and not user.is_anonymous():
                self.stdout.write("%s -> True" % arg)
            else:
                self.stdout.write("%s -> False" % arg)
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
