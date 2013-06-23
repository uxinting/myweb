#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from accounts.utils import send_activate_mail, userExist, check_mail_activate,\
    send_mail_forgetpw, check_mail_changepw
import cStringIO

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
        if request.user.is_authenticated():
            print request.user
            return HttpResponseRedirect("/")
    return render_to_response('accounts/login.html', locals(), context_instance=RequestContext(request))

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def Register(request):
    title = u'注册'
    if request.method == 'POST':
        error = {}
        try:
            label = request.POST.get('input', None)
            value = request.POST.get('value', None)
            
            if label is not None:
                #ajax check
                cdata = {label: value}
                
                if not userExist(cdata):
                    cdata['status'] = True
                    cdata['msg'] = u'可用'
                else:
                    cdata['status'] = False
                    cdata['msg'] = u'不可用'
                return HttpResponse(cdata, 'json')
            
            email = request.POST.get('email', None)
            password = request.POST.get('password1', None)
            nickname = request.POST.get('nickname', None)
            
            user = MyUser.objects.create_user(email, password, nickname)
            user.save()#注册成功
            error['msg'] = u'注册成功'
            
            #发送激活邮件
            error['msg'] += send_activate_mail(request)
        except IntegrityError:
            error['msg'] = u'重复账号，注册失败'
        except Exception, e:
            error['msg'] = u'注册失败，未知原因'
                
    return render_to_response('accounts/register.html', locals(), context_instance=RequestContext(request))

def Password(request):
    title = u'密码'
    error = {}
    if request.method == 'GET':
        if request.user.is_authenticated():#修改密码
            email = request.user.email
            changepassword = True
        else:#忘记密码
            error = check_mail_changepw(request)
            if error['status']:
                newpassword = True
                email = error['email']
                error['msg'] = u'请输入新密码'
            else:
                forgetpassword = True
    else:
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        
        if password2 and password1:#新密码提交
            try:
                if request.session['verify'] != request.POST.get('verify', None):
                    newpassword = True
                    error['msg'] = u'验证码错误'
                else:
                    user = MyUser.objects.get(email=email)
                    user.set_password(password1)
                    user.save()
                    return HttpResponseRedirect('accounts/login')
            except ObjectDoesNotExist:
                error['msg'] = u'无效的账号'
            except Exception, e:
                error['msg'] = repr(e)
        elif password1:#密码修改
            if not request.user.check_password('password1'):
                changepassword = True
                error['msg'] = u'账号用户名不匹配'
            else:
                newpassword = True
                error['msg'] = u'请输入新密码'
        else:#忘记密码
            if request.session['verify'] != request.POST.get('verify', None):
                forgetpassword = True
                error['msg'] = u'验证码错误'
            else:
                forgetpassword = True
                error['msg'] = send_mail_forgetpw(request)
        
    return render_to_response('accounts/password.html', locals(), context_instance=RequestContext(request))

def Activate(request):
    try:
        error = {}
        code = request.GET.get('code', None)
        
        if code is None:
            error['msg'] = send_activate_mail(request)
        else:
            error['msg'] = check_mail_activate(request)
            return render_to_response('accounts/activate.html', locals())
    except Exception, e:
        print e
        error['msg'] = u'邮件发送失败，请稍后再试'

    return HttpResponse(error['msg'])

def Verify(request):
    #导入三个模块
    from PIL import Image, ImageDraw, ImageFont
    import random
    '''基本功能'''
    string = '12345679ACEFGHKMNPRTUVWXYabcdefghijhklmnopqrltuvwxyz'
    #图片宽度
    img_width = 120
    #图片高度
    img_height = 28
    #背景颜色
    background = (random.randrange(230,255),random.randrange(230,255),random.randrange(230,255))
    line_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    #字号
    font_size = 23
    #加载字体
    font = ImageFont.truetype('msyh.ttf', font_size)
    #字体颜色
    font_color = ['black','darkblue','darkred']
    request.session['verify'] = ''
 
    #新建画布
    im = Image.new('RGB',(img_width,img_height),background)
    draw = ImageDraw.Draw(im)
    code = random.sample(string, 4)

    #画干扰线
    for i in range(random.randrange(3,5)):
        xy = (random.randrange(0,img_width),random.randrange(0,img_height),
              random.randrange(0,img_width),random.randrange(0,img_height))
        draw.line(xy,fill=line_color,width=1)
        
    #写入验证码文字
    x = 3
    for i in code:
        y = random.randrange(0, 5)
        draw.text((x,y), i, font=font, fill=random.choice(font_color))
        x += 30
        request.session['verify'] += i
    
    del x
    del draw
    #新图片
    newImage = Image.new('RGB', (img_width, img_height), background)
    #load像素
    newPix = newImage.load()
    pix = im.load()
    
    for y in range(0, img_height):
        offset = random.choice([-1, 0, 1])
        for x in range(0, img_width):
            #新的x坐标点
            newx = x + offset
            #你可以试试如下的效果
            #newx = x + math.sin(float(y)/10)*10
            if newx < img_width and newx > 0:
                #把源像素通过偏移到新的像素点
                newPix[newx,y] = pix[x,y]
    #保存到本地
    bufimage = cStringIO.StringIO();
    newImage.save(bufimage, 'jpeg')
    print (request.session['verify'])
    return HttpResponse(bufimage.getvalue(), 'image/jpeg')