# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Config, Branch

def contents(self):
    summary = u'�������ڴ�ī'
    currentpage = 4
    config = Config.objects.all()
    branches = Branch.objects.all()
    title = u'��ī'
    return render_to_response('calligraphy/calligraphy.html', locals())