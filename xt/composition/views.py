# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config
import os

COMPOSITIONS = os.path.join(os.path.dirname(__file__), 'compositions')

def contents(request):
    summary = u'�ŵ����Ⱥ󣬵ö�¼֮'
    contents = os.listdir(COMPOSITIONS)
    user = request.user
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'�ŵ�'
    return render_to_response('composition/contents.html', locals())

def show(request, index):
    user = request.user
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'�ŵ�'
    filename = os.listdir(COMPOSITIONS)[int(index) - 1]
    filepath = os.path.join(COMPOSITIONS, filename)
    data = open(filepath).read()
    return render_to_response('composition/show.html', locals())

def create (request):
    user = request.user
    branches = Branch.objects.all()
    config = Config.objects.get(id=1)
    title = u'�ŵ�'
    return render_to_response('composition/create.html', locals())
