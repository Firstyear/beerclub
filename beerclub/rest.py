from beerclub.models import BeerInst, Beer, Account, Drink
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import timedelta, date
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from beerclub.views import create_drink_sale

def _beer_inst_to_dict(beerinst, account=None, beerinsts=None):
    drunk = False
    if beerinsts is not None:
        #ldrinks = drinks.filter(beerinst=beerinst).count()
        #if ldrinks > 0:
        #    drunk = True
        if beerinst.id in beerinsts:
            drunk = True
    elif account is not None:
        #drinks = Drink.objects.filter(beerinst=beerinst,account=account,date__year=date.today().year).count()
        ldrinks = beerinst.drink_set.filter(account=account,date__year=date.today().year).count()
        if ldrinks > 0:
            drunk = True
    return {
            'name': beerinst.beer.name,
            'container' : beerinst.container,
            'volume' : beerinst.volume,
            'special' : beerinst.special,
            'abvp' : beerinst.beer.abvp,
            'brewery' : beerinst.beer.brewery.__unicode__(),
            'barcode' : beerinst.barcode,
            'drunk' : drunk,
            'id' : beerinst.id,
        }

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def beer_list(request):
    result = []
    #account = Account.objects.get(user=request.user)
    beerinsts = BeerInst.objects.filter(drink__account__user=request.user, drink__date__year=date.today().year).values_list('id', flat=True)
    #drinks = Drink.objects.filter(account__user=request.user, date__year=date.today().year).beerinst_set.all()
    for beer in BeerInst.objects.select_related('beer__brewery').all():
        #result[beer.id] = _beer_inst_to_dict(beer, account)
        result.append(_beer_inst_to_dict(beer, None, beerinsts))
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def beer_search(request, term=None):
    result = []
    account = Account.objects.get(user=request.user)
    beers = BeerInst.objects.filter(Q(beer__name__icontains=term) | Q(beer__brewery__name__icontains=term) | Q(barcode__contains=term) ).order_by('-stock_total')
    for beer in beers:
        #result[beer.id] = _beer_inst_to_dict(beer, account)
        result.append(_beer_inst_to_dict(beer, account))
    # This appears to "unsort" when it get's sent ... 
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def beer_search_instock(request, term=None):
    result = []
    account = Account.objects.get(user=request.user)
    beers = BeerInst.objects.filter((Q(beer__name__icontains=term) | Q(beer__brewery__name__icontains=term) | Q(barcode__contains=term) ) & Q(stock_total__gt=0) )
    for beer in beers:
        #result[beer.id] = _beer_inst_to_dict(beer, account)
        result.append(_beer_inst_to_dict(beer, account))
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def beer_detail(request, id):
    result = []
    #result = {}
    account = Account.objects.get(user=request.user)
    try:
        beer = BeerInst.objects.get(id=id)
        #result[beer.id] = _beer_inst_to_dict(beer, account)
        result.append(_beer_inst_to_dict(beer, account))
    except ObjectDoesNotExist:
        result = {'result' : -1 }
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def beer_detail_barcode(request, barcode):
    result = []
    #result = {}
    account = Account.objects.get(user=request.user)
    try:
        beer = BeerInst.objects.get(barcode=barcode)
        result.append(_beer_inst_to_dict(beer, account))
        #result[beer.id] = _beer_inst_to_dict(beer, account)
    except ObjectDoesNotExist:
        result = {'result' : -1 }
    return Response(result)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def account_current_drink_rating(request):
    result = {}
    account = Account.objects.get(user=request.user)
    drink = account.current_drink
    if drink is None:
        result['rating'] = -1
    else:
        if request.method == 'POST':
            data = request.data
            #print data
            # How will this handle errors?
            drink.rating = data['rating']
            drink.clean()
            drink.save()
        result['rating'] = drink.rating
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def account_current_drink(request):
    result = {}
    account = Account.objects.get(user=request.user)
    drink = account.current_drink
    if drink != None:
        result = {
            'id' : drink.id,
            'beer' : drink.beerinst.id,
            'rating' : drink.rating,
        }
    else:
        result = { 'result' : -1 }
    return Response(result)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def account_drinks(request):
    result = {}
    account = Account.objects.get(user=request.user)
    #time_threshold = timezone.now() - timedelta(hours=1)
    drinks = Drink.objects.filter(account=account,date__year=date.today().year).order_by('-datetime')
    if drinks != None:
        for drink in drinks:
            result[drink.id] = {
                'datetime' : drink.datetime,
                'beer_id' : drink.beerinst.id,
                'rating' : drink.rating,
            }
    else:
        result = { 'result' : -1 }
    return Response(result)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def account(request, id=None):
    result = {}
    if id is not None and request.user.is_staff:
        account = Account.objects.get(id=id)
    else:
        account = Account.objects.get(user=request.user)
    result = {
        'id' : account.id,
        'first_name' : account.user.first_name,
        'last_name' : account.user.last_name,
        'balance' : account.balance_dollars,
        'had' : account.drinks_had,
        'unique' : account.drinks_unique_had,
        'special_had' : account.special_had,
        'special_due' : account.special_due,
    }
    return Response(result)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def account_self_serve(request):
    result = { 'result' : -1 }
    account = Account.objects.get(user=request.user)
    data = request.data
    barcode = data.get('barcode', None)
    _status = None
    if barcode is not None:
        try:
            beerinst = BeerInst.objects.get(barcode=barcode)
            try:
                drink = create_drink_sale(account, beerinst, False, False, True)
                result['result'] = 0
                _status = status.HTTP_200_OK
            except Exception as e:
                result['message'] = e
        except ObjectDoesNotExist:
            result['result'] = -1
            result['message'] = 'No such barcode'
            _status = status.HTTP_406_NOT_ACCEPTABLE
    return Response(result, _status)

###############
# Add something that will display "instock but not drunk"
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def account_unique_available(request, id=None):
    #result = {}
    result = []
    if id is not None and request.user.is_staff:
        account = Account.objects.get(id=id)
    else:
        account = Account.objects.get(user=request.user)
    spec_drinks = account.drink_set.filter(date__year=date.today().year).values_list('beerinst__beer__id', flat=True).distinct()
    available_beers = BeerInst.objects.filter(stock_total__gt=0)
    available = filter(lambda x: x.beer.id not in spec_drinks, available_beers)
    for beer in sorted(available, cmp=lambda a,b: a.beer.name.lower() < b.beer.name.lower()):
        # This sorting is working, it get's "unsorted" by the json
        #This needs to become and array
        #result[beer.id] = _beer_inst_to_dict(beer, account)
        result.append(_beer_inst_to_dict(beer, account))
    return Response(result)

############
# request from Henri, get a random undrunk suggestion.
#  if specials are due, we add these and "weight them" higher in the selection.
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def account_random_unique(request, id=None):
    result = []
    if id is not None and request.user.is_staff:
        account = Account.objects.get(id=id)
    else:
        account = Account.objects.get(user=request.user)
    spec_drinks = account.drink_set.filter(date__year=date.today().year).values_list('beerinst__beer__id', flat=True).distinct()
    beer = None
    if account.special_due > 0:
        beer = BeerInst.objects.filter(stock_total__gt=0).order_by('?').first()
    else:
        beer = BeerInst.objects.filter(stock_total__gt=0, special=False).order_by('?').first()
    if beer is not None:
        result.append(_beer_inst_to_dict(beer, account))
    return Response(result)

########################################
# These are the replacement for the hand crafted api

@api_view(['GET'])
@permission_classes((IsAuthenticated, IsAdminUser))
def account_search(request, term=None):
    accounts = Account.objects.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(user__username__icontains=term))
    details = []
    map(lambda x: details.append({'id' : x.id, 'full_name': x.user.get_full_name()}), accounts)
    return Response(details)

@api_view(['GET'])
@permission_classes((IsAuthenticated, IsAdminUser))
def account_drunk(request, user_id=None, beer_id=None):
    # This may need to be account id ... 
    account = Account.objects.get(user__id=user_id)
    beerinst = BeerInst.objects.get(pk=beer_id)
    beers = beerinst.beer
    drinks = Drink.objects.filter(account=account, beerinst__beer=beers, date__year=date.today().year)
    print(drinks)
    print(account)
    print(beers)
    if len(drinks) > 0:
        return Response({'result' : True})
    else:
        return Response({'result' : False})

