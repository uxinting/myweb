# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
def about(request):
    title = u'����'
    name = u'����ͥ'
    age = 22
    university = u'���пƼ���ѧ �������ѧ�뼼��'
    return render_to_response('about/about.html', locals())