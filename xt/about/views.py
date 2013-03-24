# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
def about(request):
    title = u'关于'
    name = u'吴新庭'
    age = 22
    university = u'华中科技大学 计算机科学与技术'
    return render_to_response('about/about.html', locals())