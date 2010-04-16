#!/usr/bin/env python
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    # Main page
    url(r'^reset', views.reset, name='reset'),
#    url(r'^tellme', 'tellme', name='tellme'),
#    url(r'^frame/(?P<frame>\d+)/(?P<slot>\d)', 'frame', name='manual_frame'),
#    url(r'^cache', 'cache', name='cache'),
#    url(r'^$', 'question', name='question', kwargs={"model_components" : 5, "model_iterations" : 100 }),
)
