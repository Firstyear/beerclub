#from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from beerclub.views import AccountListView, LegendsListView, BeerListView, DrinkCreateView, AccountCreateView, StockView, BeerUniqueListView, RootView, StatsView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^accounts/$', AccountListView.as_view(), name='accounts'),
    url(r'^legends/$', LegendsListView.as_view(), name='legends' ),
    url(r'^beers/$', BeerListView.as_view(), name='beers' ),
    url(r'^beers/unique/$', BeerUniqueListView.as_view(), name='beers_unique' ),
    url(r'^drink/create/$', DrinkCreateView.as_view(), name='drink' ),
    url(r'^populate/$', AccountCreateView.as_view(), name='populate' ),
    url(r'^stock/import/$', StockView.as_view(), name='stockimport'),
    url(r'^stats/$', StatsView.as_view(), name='stats'),
    # Django rest api
    # Definetly used
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/beer_list/', 'beerclub.rest.beer_list', name='beer_list'),
    url(r'^api/beer_search_instock/(?P<term>.+)/', 'beerclub.rest.beer_search_instock', name='beer_search_instock'),
    url(r'^api/beer_search/(?P<term>.+)/', 'beerclub.rest.beer_search', name='beer_search'),
    url(r'^api/beer_detail_barcode/(?P<barcode>.+)/', 'beerclub.rest.beer_detail_barcode', name='beer_detail_barcode'),
    url(r'^api/account_self_serve/', 'beerclub.rest.account_self_serve', name='account_self_serve'),
    url(r'^api/account/(?P<id>.+)/', 'beerclub.rest.account', name='account_id'),
    url(r'^api/account_unique_available/(?P<id>.+)/', 'beerclub.rest.account_unique_available', name='account_unique_available_id'),
    url(r'^api/account_drunk/(?P<user_id>.+)/(?P<beer_id>.+)/', 'beerclub.rest.account_drunk', name='account_drunk'),
    url(r'^api/account_search/(?P<term>.+)/', 'beerclub.rest.account_search', name='account_search'),
    #Maybe unused?
    url(r'^api/account_unique_available/', 'beerclub.rest.account_unique_available', name='account_unique_available'),
    url(r'^api/account_random_unique/', 'beerclub.rest.account_random_unique', name='account_random_unique'),
    url(r'^api/account/', 'beerclub.rest.account', name='account'),
    url(r'^api/account_drinks/', 'beerclub.rest.account_drinks', name='account_drinks'),
    url(r'^api/beer_detail/(?P<id>.+)/', 'beerclub.rest.beer_detail', name='beer_detail'),
    url(r'^api/account_current_drink/', 'beerclub.rest.account_current_drink', name='account_current_drink'),
    url(r'^api/account_current_drink_rating/', 'beerclub.rest.account_current_drink_rating', name='account_current_drink_rating'),
    # Root view
    url(r'^$', RootView.as_view(), name='root'),
)
