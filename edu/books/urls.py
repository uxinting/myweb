#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('books.views',
                       url(r'^$', 'Books'),
                       url(r'share', 'Share'),
                       )
