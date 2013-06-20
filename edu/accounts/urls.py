#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
                       url(r'login', 'Login'),
                       url(r'register', 'Register'),
                       url(r'activate', 'Activate'),
                       )
