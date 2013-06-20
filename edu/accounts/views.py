#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail.message import EmailMessage

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
                    login(request, user)#登录
                    print request
                    error['msg'] = u'成功'
                else:
                    error['msg'] = u'您的账号尚未激活'
                    error['href'] = u'javascript:activate();'
                    error['more'] = u'发送激活邮件'
            else:#user is None, password is incorrect
                error['msg'] = u'账号密码不匹配'
                
        except ObjectDoesNotExist:
            error['msg'] = u'无效的账号'
        
    else:#request method is get
        error['msg'] = u''
        next = request.path.encode('utf-8')
        if next.startswith('/accounts'):
            next = '/'
    return render_to_response('accounts/login.html', locals(), context_instance=RequestContext(request))

def Register(request):
    title = u'注册'
    
    return render_to_response('accounts/register.html', locals(), context_instance=RequestContext(request))

def Activate(request):
    try:
        email = request.GET.get('email', None)

        if email is None:
            info = u'无效的邮件地址'
        else:
            msg = EmailMessage('edu激活邮件',
                              '<br><a href="http://localhost:8090/acounts/activate">点击激活账号</a>',
                              'edu_server@sina.cn', 
                              [email]
                               )
            msg.content_subtype = 'html'
            msg.send(False)
            info = u'激活邮件已发送，请注意查看邮箱'
    except Exception, e:
        info = u'邮件发送失败，请稍后再试'

    return HttpResponse(info)