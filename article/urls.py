from django.conf.urls import patterns, include, url

'''
Created on 2013-5-8

@author: Administrator
'''
urlpatterns = patterns('article.views',
                       url(r'^$', 'article'),
                       )