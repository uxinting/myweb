#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('books.views',
                       url(r'^$', 'Books'),
                       url(r'^/(\d+)/$', 'Chapters'),
                       url(r'^/chapter/(\d+)/$', 'BookChapter'),
                       url(r'share', 'Share'),
                       )
