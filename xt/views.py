# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from httplib import HTTPResponse
from django.contrib.auth.forms import UserCreationForm
from xt.models import UserProfile
from xt.models import Branch, Config
from xt import settings

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
    title = u'登录'
    isloginhtml = 'yes'
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
           return HttpResponse('exception ' + request.POST)
    else:
        return HttpResponse(request.method)
#    return render_to_response('xt/login.html', locals())

def register(request):
    title = u'注册'
    if request.method == 'POST':
        try:
            username = request.POST['username']
            last_name = request.POST['last_name']
            email = request.POST.get('email', '')
            password = request.POST['password']
            
            major = request.POST.get('major', '')
            favor = request.POST.get('favor', '')
            law = request.POST.get('law', '')
            
            user = auth.models.User.objects.create_user(username, email, password)
            if user is not None:
                user.last_name = last_name
                auth.login(request, user)
                user.save()
            
            profile = UserProfile.objects.create(user=user, major=major,
                                                 favor=favor, law=law)
            if profile is not None:
                profile.save()
            
            return HttpResponseRedirect('/')
        except:
            pass
    else:
        pass
        
    return render_to_response('xt/register.html')

def message(request):
    if (request.method == 'POST'):
        subject = request.POST.get('subject', '')
        contents = request.POST.get('contents', '')
        
        if (not subject or not contents):
            return HttpResponseRedirect(request.path)
        
        return render_to_response('xt/message.html', locals())
    else:
        return HttpResponseRedirect(request.path)