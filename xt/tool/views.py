# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response

def tools(request):
    title = u'以用'
    summary = u'以利器善公之事'
    return render_to_response('tool/tools.html', locals())
