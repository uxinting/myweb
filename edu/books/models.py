#-*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class Book(models.Model):
    
    #书名
    name    = models.CharField(max_length=255)
    #书作者
    author  = models.CharField(max_length=128)
    #分享者
    sharer  = models.CharField(max_length=64)
    #所在路径
    path    = models.FilePathField()
    #分享日期
    date  = models.DateTimeField(default=timezone.now())
    #权限
    priv    = models.IntegerField(default=0)
    #描述
    desc    = models.TextField()
    
    class Meta:
        db_table = 'book'
    
class Chapter(models.Model):
    '''章节'''
    #章节名
    subject = models.CharField()
    #所在书籍名
    book    = models.ForeignKey(Book)
    #第几章
    index = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'chapter'