'''
Created on 2013-3-23

@author: xinting
'''
from django.conf.urls import patterns, include, url

urlpatterns = patterns('xt.about.views',
                       url('^$', 'about'),
                       )