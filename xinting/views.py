#-*- coding: utf-8 -*-
'''
Created on 2013-4-29

@author: Administrator
'''
from django.shortcuts import render_to_response
def welcome(request):
    title = u'Welcome'
    return render_to_response('welcome.html', locals())