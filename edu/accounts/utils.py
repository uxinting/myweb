#-*- coding: utf-8 -*-
import base64, hashlib, time
import accounts
from django.core.mail.message import EmailMultiAlternatives
from django.db import connection
from accounts.models import MyUser

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
    text_content = u'感谢您注册edu请点击链接激活您的账号该链接有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时'
    html_content = u'<p>感谢您注册edu</p><p>请<a href="' + url + u'">点击链接</a>激活您的账号</p><p>该链接有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时</p>'
    
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
    text_content = u'请点击链接修改您的账号对应的密码'
    html_content = u'<p>请<a href="' + url + u'">点击链接</a>修改您的账号对应的密码</p>'
    
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
        raise e