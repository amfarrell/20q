from django.conf.urls.defaults import *
import games
from views import style,script
import old # XXX remove this after we have successfully gottent the old site up and running and understood it.

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^test20q/', include('test20q.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^admin/', include(admin.site.urls)),
    (r'^test/', include('games.urls')),
    (r'^old/', include('old.urls')),
    (r'style/(.+)$', style),
    (r'script/(.+)$', script),
)
