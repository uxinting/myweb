#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from xinting import settings
import os

ARTICLE = os.path.join(settings.MEDIA_ROOT, 'article')

def article(request):
    title = 'Article'
    articles = []
    if request.GET.get('title', None) is None:
        for t in os.listdir(ARTICLE):
            path = os.path.join(ARTICLE, t)
            contents = []
            contents.append(open(path).readline())
            articles.append({'title': t, 'contents': contents})
    else:
        t = request.GET.get('title', None).encode('utf-8')
        path = os.path.join(ARTICLE, t)
        contents = open(path).readlines()
        articles.append({'title': t, 'contents': contents})
        all = True
    return render_to_response('article/article.html', locals())