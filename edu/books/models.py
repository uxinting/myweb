#-*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from accounts.models import MyUser

class Book(models.Model):
    
    #书名
    name    = models.CharField(max_length=255)
    #书作者
    author  = models.CharField(max_length=128)
    #分享者
    sharer  = models.ForeignKey(MyUser)
    #所在路径
    path    = models.FilePathField()
    #分享日期
    date    = models.DateTimeField(default=timezone.now())
    #权限
    priv    = models.IntegerField(default=0)
    #热度
    pop     = models.IntegerField(default=0)
    #描述
    desc    = models.TextField()
    
    class Meta:
        db_table = 'book'
    
class Chapter(models.Model):
    '''章节'''
    #章节名
    subject = models.CharField(max_length=255)
    #所在书籍名
    book    = models.ForeignKey(Book, blank=True)
    #文章中德position
    index = models.PositiveIntegerField()
    endindex = models.IntegerField()
    
    class Meta:
        db_table = 'chapter'
        