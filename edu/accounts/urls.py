#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
                       url(r'login', 'Login'),
                       url(r'logout', 'Logout'),
                       url(r'register', 'Register'),
                       url(r'activate', 'Activate'),
                       url(r'password', 'Password'),
                       url(r'verify', 'Verify'),
                       )
