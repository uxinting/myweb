# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from httplib import HTTPResponse
from django.contrib.auth.forms import UserCreationForm
from xt.models import UserProfile
from xt.models import Branch, Config
from xt import settings
from django.core.mail import mail_admins, send_mail

def welcome(request):
    branches = Branch.objects.all()
    currentpage = 1;
    config = Config.objects.get(id=1)
    title = branches.get(id=currentpage).name
    summary = branches.get(id=currentpage).summary
    user = request.user
    return render_to_response('xt/welcome.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def login(request):
    title = u'初见'
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            if (request.POST.get('remeber-me', '') == 'on'):
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            else:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('xt/login.html', locals())
        except:
           pass
    else:
        return render_to_response('xt/login.html', locals())

def register(request):
    title = u'初会'
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['e-mail']
            password = request.POST['password']
            
            last_name = request.POST.get('nickname', '')
            major = request.POST.get('major', '')
            favor = request.POST.get('favor', '')
            maxim = request.POST.get('maxim', '')
            
            user = auth.models.User.objects.create_user(username, email, password)
            if user is not None:
                user.last_name = last_name
                user.save()
            
            userprofile = UserProfile.objects.create(user=user, major=major,favor=favor, maxim=maxim)
            if not userprofile:
                userprofile.save()
            
            return HttpResponseRedirect('/')
        except:
            pass
    else:
        return render_to_response('xt/register.html')

def message(request):
    if (request.method == 'POST'):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        if (not subject or not message):
            return HttpResponseRedirect(request.path)
        
        try:
            mail_admins(subject, message)
        except:
           pass
        
        return render_to_response('xt/message.html', locals())
    else:
        return HttpResponseRedirect(request.path)