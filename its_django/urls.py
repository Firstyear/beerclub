from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
admin.autodiscover()
#from django.views.generic import TemplateView
from beerclub.views import RootView

urlpatterns = [
    # Examples:
    # url(r'^$', 'its_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', auth_views.login, {'template_name': 'beerclub/login.html', 'extra_context': {'next':'/bc/'} }, name="accounts_login"),
    url(r'^accounts/logout/', auth_views.logout, {'next_page': '/', 'template_name': 'beerclub/logout.html'}, name="accounts_logout"),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^bc/', include('beerclub.urls', namespace='beerclub')),
    url(r'^', include('beerclub.urls', namespace='beerclub_root')),
    #url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'beerclub/login.html', 'extra_context': {'next':'/bc/'} }, name="root_accounts_login"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
