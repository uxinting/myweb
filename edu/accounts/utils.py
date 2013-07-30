#-*- coding: utf-8 -*-
import base64, hashlib, time
import accounts
from django.core.mail.message import EmailMultiAlternatives
from django.db import connection
from accounts.models import MyUser
import re

def html_to_text(html):
    return ''.join(re.findall(r'(?<=>).*?(?=<)', html))

def send_activate_mail(request):
    '''发送一个激活邮件到email所指定的地址，函数返回一个校验码，以后核对.
            将email用base64编码，并加入当时的的时间float格式的md5编码与其中
    '''
    
    to = request.GET.get('email', None)
    
    #判断此邮箱是否已注册
    if not userExist({'email': to}):
        return u'无效的邮件地址'
    
    #判断request中是否已有激活码
    if request.session.get('activate', None):
        return u'激活邮件已发送，请查看收件箱或垃圾箱'
    
    email = base64.b64encode(to)
    code = hashlib.md5(repr(time.time())).hexdigest()
    
    url = accounts.ACTIVATE_URL + '?email=' + email + '&code=' + code
    print url
    #text_content = u'感谢您注册edu请点击链接激活您的账号该链接有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时'
    html_content = u'<p>感谢您注册edu</p><p>请<a href="' + url + u'">点击链接</a>激活您的账号</p><p>该链接有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时</p>'
    text_content = html_to_text(html_content)
    print html_content,  text_content
    
    msg = EmailMultiAlternatives(accounts.ACTIVATE_MAIL_SUBJECT, text_content, accounts.ACTIVATE_MAIL_FROM, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception, e:
        return repr(e)
    
    request.session['activate'] = {'email': email, 'code': code}
    request.session.set_expiry(accounts.ACTIVATE_MAIL_EXPIRE * 3600)
    return u'激活邮件已发送，请注意查看邮箱'

def check_mail_activate(request):
    try:
        email = request.GET.get('email', None)
        code = request.GET.get('code', None)
        
        activate = request.session.get('activate', None)
        if activate is None:
            return u'激活邮件已经失效'
        
        if activate.get('email', None) == email and activate.get('code', None) == code:
            user = MyUser.objects.get(email=base64.b64decode(email))
            user.is_active = True
            user.save()
            request.session.flush()#清除session
    except Exception, e:
        return repr(e)
    
    return u'激活成功'

def send_mail_forgetpw(request):
    to = request.POST.get('email', None)
    
    if not userExist({'email': to}):
        return u'无效的账号'
    
    email = base64.b64encode(to)
    code = MyUser.objects.get(email=to).password.replace('+', '%2B')
    
    url = accounts.CHANGEPW_URL + '?email=' + email + '&code=' + code
    html_content = u'<p>请<a href="' + url + u'">点击链接</a>修改您的账号对应的密码</p>'
    text_content = html_to_text(html_content)
    
    msg = EmailMultiAlternatives(accounts.CHANGEPW_MAIL_SUBJECT, text_content, accounts.MAIL_FROM, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception, e:
        return repr(e)
    return u'修改密码邮件已发送，请注意查看邮箱'

def check_mail_changepw(request):
    f = request.GET.get('email', None)
    if not f:
        return {'status': False, 'msg': u'请输入账号'}
    email = base64.b64decode(f)
    password = request.GET.get('code', None)
    
    if not userExist({'email': email}):
        return {'status': False, 'msg': u'无效的链接，账号错误'}
    print MyUser.objects.get(email=email).password, password
    if MyUser.objects.get(email=email).password != password:
        return {'status': False, 'msg': u'无效的链接'}
    
    return {'status': True, 'msg': '', 'email': email}

def check_register_parameter(request):
    email = request.POST.get('email', None)
    password1 = request.POST.get('password1', None)
    password2 = request.POST.get('password2', None)
    nickname = request.POST.get('nickname', None)
    
    email_re = r'^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
    password_re = r'^[\_\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{8,22}$'
    nickname_re = r'^[a-zA-Z0-9\_]{4,16}$'
    
    if not re.match(email_re, email):
        raise Exception(u'邮箱名非法')
    
    if password1 != password2:
        raise Exception(u'密码不一致')
    
    if not re.match(password_re, password1):
        raise Exception(u'密码非法')
    
    if not re.match(nickname_re, nickname):
        raise Exception(u'昵称非法')

def check_password_new(request):
    password1 = request.POST.get('password1', None)
    password2 = request.POST.get('password2', None)
    
    password_re = r'^[\_\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{8,22}$'
    
    if password1 != password2:
        raise Exception(u'密码不一致')
    
    if not re.match(password_re, password1):
        raise Exception(u'密码非法')
    
def check_verify(request):
    verify = request.POST.get('verify', None)
    if not verify:
        raise Exception(u'未输入验证码')
    
    verify_s = request.session.get('verify', None)
    if not verify_s:
        raise Exception(u'无效的验证码')
    
    if verify != verify_s:
        raise Exception(u'验证码错误')

def userExist(p):
    '''p中必须有一个属性key对应的value作为where条件'''
    try:
        ps = p.items()
        table = accounts.AUTH_USER_MODEL.lower().replace('.', '_')
        sql = 'select * from ' + table + ' where '+ ps[0][0] + '=' + '\'' + ps[0][1] + '\''
        for k, v in ps[1:]:
            sql = sql + ' and ' + k + '=' + '\'' + v + '\''
        if connection.cursor().execute(sql) == 0:
            return False
        else:
            return True
    except Exception, e:
        print 'userexist', e
        raise e