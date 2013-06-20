#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

def Login(request):
    title = u'登录'
    error = {}
    if request.method == 'POST':
        try:
            email = request.POST.get('email', None)
            MyUser.objects.get(email=email)
            user = authenticate(email=email, password=request.POST.get('password', None))
            
            if user is not None:
                if  user.is_active:
                    print request.path
                    error['msg'] = u'成功'
                else:
                    error['msg'] = u'您的账号尚未激活'
                    error['href'] = u'acitve'
                    error['more'] = u'激活账号'
            else:#user is None, password is incorrect
                error['msg'] = u'账号密码不匹配'
                
        except ObjectDoesNotExist:
            error['msg'] = u'无效的账号'
        
    else:#request method is get
        error['msg'] = u''
    return render_to_response('accounts/login.html', locals(), context_instance=RequestContext(request))