# _*_ coding: gb2312 _*_
from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=30)
    summary = models.CharField(max_length=64)
    responsehtml = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name

class Config(models.Model):
    registered = models.IntegerField()
    limit = models.IntegerField()
    
    def __unicode__(self):
        return u'系统设置'

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    major = models.CharField(max_length=255)
    favor = models.CharField(max_length=255)
    law = models.TextField()
    personal = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'用户信息'
