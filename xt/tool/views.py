# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config

def tools(request):
    title = u'����'
    summary = u'�������ƹ�֮��'
    branches = Branch.objects.all()
    config = Config.objects.all()
    return render_to_response('tool/tools.html', locals())
