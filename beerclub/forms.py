from django import forms
from beerclub.models import Drink

class DrinkForm(forms.Form):
    name = forms.CharField(max_length=255)
    payee_name = forms.CharField(max_length=255, required=False)
    beer = forms.CharField(max_length=255, required=False)
    name_pk = forms.IntegerField(initial=0)
    payee_name_pk = forms.IntegerField(initial=0, required=False)
    beer_pk = forms.IntegerField(initial=0)
    value = forms.CharField(initial=0, required=False)
    free = forms.BooleanField(required=False)
    special = forms.BooleanField(required=False)

class AccountCreateForm(forms.Form):
    name = forms.CharField(max_length=255)
    #name_pk = forms.IntegerField()
    #barcode = forms.CharField(max_length=255)

class StockCreateForm(forms.Form):
    barcode = forms.CharField(max_length=255, widget=(forms.TextInput(attrs={'autofocus':'autofocus'})))
