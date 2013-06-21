#-*- coding: utf-8 -*-
import base64, hashlib, time
import accounts
from django.core.mail.message import EmailMultiAlternatives
from django.db import connection

def send_activate_mail(to):
    '''发送一个激活邮件到email所指定的地址，函数返回一个校验码，以后核对.
            将email用base64编码，并加入当时的的时间float格式的md5编码与其中
    '''
    email = base64.b64encode(to)
    code = hashlib.md5(repr(time.time())).hexdigest()
    
    url = accounts.ACTIVATE_URL + '?email=' + email + '&code=' + code
    text_content = u'感谢您注册edu请点击链接激活您的账号账号有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时'
    html_content = u'<p>感谢您注册edu</p><p>请<a href="' + url + u'">点击链接</a>激活您的账号</p><p>账号有效期' + repr(accounts.ACTIVATE_MAIL_EXPIRE) + u'小时</p>'
    
    msg = EmailMultiAlternatives(accounts.ACTIVATE_MAIL_SUBJECT, text_content, accounts.ACTIVATE_MAIL_FROM, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception, e:
        raise e
    
    return {'email': email, 'code': code}

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