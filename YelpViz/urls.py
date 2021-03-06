from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'business.views.home', name='home'),
    url(r'^get_businesses', 'business.views.get_businesses'),
    url(r'^get_reviews', 'business.views.get_reviews'),
    url(r'^compare_businesses', 'business.views.compare_businesses')
)
