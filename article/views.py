#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def article(request):
    title = 'Article'
    return render_to_response('article/article.html', locals())