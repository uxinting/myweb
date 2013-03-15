# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config
import os

COMPOSITIONS = os.path.join(os.path.dirname(__file__), 'compositions')

def contents(request):
    summary = u'闻道有先后，得而录之'
    contents = os.listdir(COMPOSITIONS)
    # user = request.user
    currentpage = 2;
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'闻道'
    return render_to_response('composition/article.html', locals())

def show(request, index):
    # user = request.user
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'闻道'
    filename = os.listdir(COMPOSITIONS)[int(index) - 1]
    filepath = os.path.join(COMPOSITIONS, filename)
    datas = open(filepath).readlines()
    nxt = len(os.listdir(COMPOSITIONS)) > int(index) and repr(int(index) + 1) or repr(int(index))
    prev = int(index) <= 1 and repr(int(index)) or repr(int(index) - 1)
    return render_to_response('composition/article-show.html', locals())

def create (request):
    user = request.user
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'闻道'
    return render_to_response('composition/create.html', locals())
