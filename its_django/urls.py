from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
#from django.views.generic import TemplateView
from beerclub.views import RootView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'its_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'beerclub/login.html', 'extra_context': {'next':'/bc/'} }, name="accounts_login"),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', {'next_page': '/', 'template_name': 'beerclub/logout.html'}, name="accounts_logout"),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^bc/', include('beerclub.urls', namespace='beerclub')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'beerclub/login.html', 'extra_context': {'next':'/bc/'} }, name="root_accounts_login"),
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
