#-*- coding: utf-8 -*-
from django.http import HttpResponse

def Modify(request):
    return HttpResponse('ok', 'text/plain')