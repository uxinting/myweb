#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
'''
Created on 2013-5-14

@author: Administrator
'''
urlpatterns = patterns('calligraphy.views',
                       url(r'^$', 'calligraphy'),
                       )