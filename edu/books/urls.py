#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('books.views',
                       url(r'^$', 'Books'),
                       url(r'^/(\d+)/$', 'Chapters'),
                       url(r'^/chapter/(\d+)/$', 'BookChapter'),
                       url(r'^/chapter/(\d+)/next', 'BookChapterNext'),
                       url(r'^/chapter/(\d+)/prev', 'BookChapterPrev'),
                       url(r'^/chapter/create', 'BookChapterCreate'),
                       url(r'^/chapter/remove', 'BookChapterRemove'),
                       
                       url(r'^/(\d+)/reviews/$', 'Reviews'),
                       url(r'^/review/(\d+)/$', 'BookReview'),
                       url(r'^/(\d+)/review/create/$', 'BookReviewCreate'),
                       url(r'^/review/remove', 'BookReviewRemove'),
                       url(r'share', 'Share'),
                       )
