#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def Login(request):
    title = u'登录'
    return render_to_response('accounts/login.html')