from django.core.management.base import BaseCommand, CommandError 
from beerclub.models import Stock, StockTake, StockWriteOff, BeerInst
from django.contrib.auth.models import User
from django.db import transaction, models

class Command(BaseCommand):
    args = ''
    help = 'Merges two beers into each other, but leaves all BeerInsts attached.'

    def _reconcile(self):
        for bi in BeerInst.objects.all():
            bi.reconcile_stock()

    def _cleanup(self):
        for st in StockTake.objects.all():
            st.delete()

    def _collect_inventory(self):
        while True:
            val = raw_input("barcode, SHOW or 'END'. # ")
            if val == 'END':
                return
            elif val == 'SHOW':
                for sto in StockTake.objects.all():
                    print(sto)
            else:
                beerinst_pack = BeerInst.objects.filter(barcode_pack=val).first()
                beerinst_sing = BeerInst.objects.filter(barcode=val).first()
                if beerinst_pack is not None:
                    st = StockTake(beerinst=beerinst_pack, quantity=beerinst_pack.quantity_pack)
                    st.clean()
                    st.save()
                    print(st)
                    last = st
                elif beerinst_sing is not None:
                    st = StockTake(beerinst=beerinst_sing, quantity=1)
                    st.clean()
                    st.save()
                    print(st)
                    last = st
                else:
                    print('NO SUCH BEER')

    def _coalesce(self):
        # Get the set of all beerinsts referenced by
        for bi in BeerInst.objects.all():
            quantity = StockTake.objects.filter(beerinst=bi).aggregate(quantity=models.Sum('quantity'))['quantity']
            if quantity > 0:
                StockTake.objects.filter(beerinst=bi).delete()
                st = StockTake(beerinst=bi, quantity=quantity)
                st.clean()
                st.save()

    def _compare_stock(self):
        actions = {'add': [], 'write off': []}
        # * We retrieve the current set of Stock.
        stock = set(BeerInst.objects.filter(stock_total__gt=0))
        stocktake = set(map(lambda st: st.beerinst, StockTake.objects.all()))
        # ** Stock that exists, but not in the stocktake, has Stock Objects Created.
        # ** Extraneous Stock Objects that do not exist in the StockTake, Have a StockWriteOff created with comment
        for bi in stock | stocktake:
            st = StockTake.objects.filter(beerinst=bi).first()
            if st is not None:
                if st.quantity > bi.stock_total:
                    # OKAY: So, there are cases where if you have negative stock, and then you stock take
                    # This number may be more than you think. IE, you have -1 drink, you stock take the 6 pack
                    # then it wants to add 7 bottles.
                    # Stock take isn't assuming past behaviour, it's fixing numbers for what you have RIGHT MEOW
                    # So if you scan in that six pack, but one was drunk, forcing the -1, you're fucking it up
                    # You should scan in only 5 of the bottles, as that's what you have, and the math below will add
                    # the extra 1 to fix it. 
                    #if bi.stock_total < 0:
                    #    actions['add'].append( (bi , st.quantity - (bi.stock_total * -1)) )
                    #else:
                    actions['add'].append( (bi , st.quantity - bi.stock_total))
                elif st.quantity < bi.stock_total:
                    actions['write off'].append((bi, bi.stock_total - st.quantity ))
                else:
                    pass
            else:
                # We have stock that needs write off
                actions['write off'].append((bi, bi.stock_total ))
        return actions

    def _display_act(self, actions):
        print("Will ADD:")
        for act in actions['add']:
            print(act)
            print(" * %s -+> %s" % act)
        print("Will WRITE OFF:")
        for act in actions['write off']:
            print(act)
            print(" * %s <-- %s" % act)

    def _apply_actions(self, actions):
        for act in actions['add']:
            st = Stock(beerinst=act[0], quantity=act[1], comment="Stock take addition")
            st.save()
            print("%s \n" % st)
        for act in actions['write off']:
            sw = StockWriteOff(beerinst=act[0], quantity=act[1], comment="Stock take removal")
            sw.save()
            print("%s \n" % sw)
        # * A further reconcilation is triggered.
        self._reconcile()
        self._validate_complete()
        # * The set of numbers from both are compared again, and if they are correct, stock take is over

    def _negative_check(self):
        #This check seems broken .... 
        bi = BeerInst.objects.filter(stock_total__lt=0)
        if bi is not None:
            print("\n\nWARNING: SOME BEERS ARE IN NEGATIVE STOCK\n\n")
            for b in bi:
                print("%s : %s" % (b, b.stock_total))
            print("\n\nYOU LIKELY HAVE STOCK THAT HAS BEEN PURCHASED BUT NOT INVENTORIED")
            print("RUN manage.py negative_stock_fix TO AUTOMATICALLY POPULATE THESE\n\n")
            print("YOU SHOULD DO THIS BEFORE STOCK TAKE\n\n")

    def _validate_complete(self):
        actions = self._compare_stock()
        if len(actions['add']) != 0 or len(actions['write off']) != 0:
            print('\n\nINCOMPLETE - ERROR\n\n')
            self._display_act(actions)
            raise(Exception("ROLLING BACK ALL ACTIONS"))
        else:
            print("\n\nCOMPLETE\n\n")
            self._negative_check()

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if raw_input("ARE YOU READY TO STOCK TAKE!!! TYPE 'YES' # ") != "YES":
            return

        #Stock take needs to occur in a couple of steps.
        # * A reconciliation is triggered.
        self._cleanup()
        self._reconcile()
        self._negative_check()
        # * the current inventory must be collected.
        self._collect_inventory()
        self._coalesce()
        actions = self._compare_stock()

        self._display_act(actions)
        if raw_input("CONTINUE? 'YES': ") == 'YES':
            self._apply_actions(actions)
        else:
            print("\n\nCANCELLED\n\n")
        # Delete the StockTake objects
        self._cleanup()

