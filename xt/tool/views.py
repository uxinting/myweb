# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response

def tools(request):
    title = u'����'
    summary = u'�������ƹ�֮��'
    return render_to_response('tool/tools.html', locals())
