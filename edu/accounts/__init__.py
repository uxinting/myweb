#-*- coding: utf-8 -*-
ACTIVATE_URL = 'http://127.0.0.1:8090/accounts/activate'
ACTIVATE_MAIL_EXPIRE = 1 #hour
ACTIVATE_MAIL_SUBJECT = u'邮件激活'
ACTIVATE_MAIL_FROM = 'edu_server@sina.cn'
AUTH_USER_MODEL = 'accounts.MyUser'

CHANGEPW_URL = 'http://127.0.0.1:8090/accounts/password'
CHANGEPW_MAIL_EXPIRE = 3 #hour
CHANGEPW_MAIL_SUBJECT = u'修改密码'
MAIL_FROM = 'edu_server@sina.cn'