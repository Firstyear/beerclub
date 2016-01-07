from django.contrib import admin
from datetime import date, timedelta

from beerclub.models import Beer, BeerInst, Drink, Payment, Account, Brewery, Expenditure, Stock, StockWriteOff
# Register your models here.

class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('cost', 'comment')

class BeerInstAdmin(admin.ModelAdmin):
    fields = ('beer', 'container', 'volume', 'unit_sale_price', 'special', 'barcode', 'barcode_pack', 'quantity_pack')
    list_display = ('beer', 'container', 'volume', 'unit_sale_price', 'stock_total', 'stock_value')
    search_fields = ['beer__name', 'beer__brewery__name', 'barcode', 'barcode_pack']
    ordering = ('-stock_total', 'beer__name')

class BeerInstInLine(admin.TabularInline):
    model = BeerInst
    fields = ('container', 'volume', 'unit_sale_price', 'special', 'barcode', 'barcode_pack', 'quantity_pack')
    extra = 0

class BeerAdmin(admin.ModelAdmin):
    fields = ('name', 'brewery', 'abvp')
    list_display = ('name', 'brewery', 'abvp')
    search_fields = ['name', 'brewery__name']
    inlines = [
        BeerInstInLine
    ]

class BeerInLine(admin.TabularInline):
    model = Beer
    fields = ('name', 'abvp')
    extra = 0

class DrinkAdmin(admin.ModelAdmin):
    #fields = ('account', 'beer', 'debt', 'special', 'date')
    list_display = ('account', 'beerinst', 'datetime', 'debt', 'special', 'selfserve')
    #readonly_fields = ('date',)
    search_fields = ['account__user__first_name', 'account__user__last_name']

class DrinkInLine(admin.TabularInline):
    model = Drink
    fields = ('beerinst', 'debt', 'special')
    extra = 0
    #readonly_fields = ('date',)
    def get_queryset(self, request):
        qs = super(DrinkInLine, self).get_queryset(request)
        return qs.filter(datetime__year=date.today().year)

class PaymentAdmin(admin.ModelAdmin):
    fields = ('account', 'date', 'value')
    list_display = ('account', 'date', 'value')
    search_fields = ['account__user__first_name', 'account__user__last_name']
    readonly_fields = ('date',)

class PaymentInLine(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ('account', 'value')
    #readonly_fields = ('date',)
    def get_queryset(self, request):
        qs = super(PaymentInLine, self).get_queryset(request)
        enddate = date.today()
        startdate = enddate - timedelta(days=14)
        return qs.filter(date__range=[startdate, enddate]).order_by("date")

class AccountAdmin(admin.ModelAdmin):
    #fields = ('user')
    list_display = ('__unicode__', 'balance_dollars', 'special_due', 'active')
    search_fields = ['user__first_name', 'user__last_name']
    #inlines = [
    #        #DrinkInLine,
    #        #PaymentInLine,
    #        ]

class BreweryAdmin(admin.ModelAdmin):
    inlines = [ BeerInLine ]

class StockAdmin(admin.ModelAdmin):
    pass

class StockWriteOffAdmin(admin.ModelAdmin):
    pass

admin.site.register(Expenditure, ExpenditureAdmin)

admin.site.register(Brewery, BreweryAdmin)
admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerInst, BeerInstAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockWriteOff, StockWriteOffAdmin)
