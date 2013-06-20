#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail.message import EmailMultiAlternatives

def Login(request):
    title = u'登录'
    error = {}
    if request.method == 'POST':
        try:
            email = request.POST.get('email', None)
            MyUser.objects.get(email=email)
            user = authenticate(email=email, password=request.POST.get('password', None))
            
            if user is not None:
                if user.is_active:
                    login(request, user)#登录
                    return HttpResponseRedirect(request.POST.get('next', '/'))
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
        
        code = request.GET.get('code', None)

        if code is None:
            import time, hashlib
            code = hashlib.md5(repr(time.time())).hexdigest()
            request.session['code'] = code
            request.session['email'] = email
        else:
            error = {}
            if code == request.session.get('code', None):
                try:
                    user = MyUser.objects.get(email=request.session.get('email', None))
                    user.is_active = True
                    user.save()
                    del request.session['code']
                except Exception, e:
                    print e
                error['msg'] = u'成功激活账号'
            else:
                error['msg'] = u'无颜的激活邮件链接'
            return render_to_response('accounts/activate.html', locals())

        if email is None:
            info = u'无效的邮件地址'
        else:
            subject, from_email, to = 'edu 激活邮件', 'edu_server@sina.cn', email
            text_content = '点击激活账号'
            html_content = '<p><a href="http://127.0.0.1:8090/accounts/activate?code=' + code + '">点击</a>激活账号</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            info = u'激活邮件已发送，请注意查看邮箱'
    except Exception, e:
        print e
        info = u'邮件发送失败，请稍后再试'

    return HttpResponse(info)