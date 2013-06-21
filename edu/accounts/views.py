#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from accounts.utils import send_activate_mail, userExist
import accounts

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
        if request.user is not None:
            return HttpResponseRedirect("/")
        error['msg'] = u''
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
    return render_to_response('accounts/login.html', locals(), context_instance=RequestContext(request))

def Register(request):
    title = u'注册'
    if request.method == 'POST':
        error = {}
        try:
            input = request.POST.get('input', None)
            value = request.POST.get('value', None)
            
            if input is not None:
                import json
                #ajax check
                cdata = {input: value}
                
                if not userExist(cdata):
                    cdata['status'] = True
                    cdata['msg'] = u'可用'
                else:
                    cdata['status'] = False
                    cdata['msg'] = u'不可用'
                return HttpResponse(json.dumps(cdata))
            
            email = request.POST.get('email', None)
            password = request.POST.get('password1', None)
            nickname = request.POST.get('nickname', None)
            
            user = MyUser.objects.create_user(email, password, nickname)
            user.save()#注册成功
            error['msg'] = u'注册成功'
            
            #发送激活邮件
            request.session['activate'] = send_activate_mail(email)
            request.session.set_expiry(accounts.ACTIVATE_MAIL_EXPIRE * 3600)
        except IntegrityError:
            error['msg'] = u'重复账号，注册失败'
        except Exception, e:
            error['msg'] = u'注册失败，未知原因'
                
    return render_to_response('accounts/register.html', locals(), context_instance=RequestContext(request))

def Activate(request):
    import base64
    try:
        error = {}
        email = request.GET.get('email', None)
        code = request.GET.get('code', None)
        
        if not userExist({'email': base64.b64decode(email)}):
            info = u'无效的邮件地址'
            email = None
        
        if code is None:
            if email is not None:
                request.session['activate'] = send_activate_mail(email)
                request.session.set_expiry(accounts.ACTIVATE_MAIL_EXPIRE * 3600)
                info = u'激活邮件已发送，请注意查看邮箱'
        else:
            activate = request.session['activate']
            print activate, email, code
            if code == activate.get('code', None) and email == activate.get('email', None):
                try:
                    user = MyUser.objects.get(email=base64.b64decode(email))
                    user.is_active = True
                    user.save()
                    error['msg'] = u'成功激活账号'
                    request.session.flush()#清除session
                except Exception, e:
                    print e
                    error['msg'] = u'激活出错'
            else:
                error['msg'] = u'无效的激活邮件链接'
            return render_to_response('accounts/activate.html', locals())
    except Exception, e:
        print e
        info = u'邮件发送失败，请稍后再试'

    return HttpResponse(info)