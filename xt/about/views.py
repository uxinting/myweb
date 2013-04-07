# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import UserProfile
from django.contrib.auth.models import User
def about(request):
    me = User.objects.get(id=1)
    profile = me.get_profile()
    title = u'关于'
    return render_to_response('about/about.html', locals())