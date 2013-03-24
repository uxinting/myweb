# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config

def tools(request):
    title = u'以用'
    summary = u'以利器善公之事'
    branches = Branch.objects.all()
    config = Config.objects.all()
    return render_to_response('tool/tools.html', locals())
