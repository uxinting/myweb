'''
Created on 2013-3-24

@author: xinting
'''
from django.conf.urls import patterns, include, url

urlpatterns = patterns('xt.tool.views',
                       url('^$', 'tools'),
                       url('^upload/$', 'upload'),
                       )