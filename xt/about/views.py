#_*_ coding: gb2312 _*_
'''
Created on 2013-3-23

@author: xinting
'''
from django.shortcuts import render_to_response
def about(request):
    title = u'关于'
    return render_to_response('about/about.html', locals())