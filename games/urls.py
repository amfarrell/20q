from django.conf.urls.defaults import *
import views

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
    (r'^first/', views.first),
    (r'^answerQuestion', views.acceptAnswer),
    # look at the virualenv at @amemone:/srv/commons
    # evaluator.py imports some stuff from there
    (r'',views.postQuestion),
)
