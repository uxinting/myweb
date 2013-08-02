#-*- coding: utf-8 -*-
from django.db import models
from accounts.models import MyUser
from django.utils import timezone
from books.models import Book, Chapter

class Reader(models.Model):
    user = models.OneToOneField(MyUser)
    
    #字体
    fontFamily  = models.CharField(max_length=16, default=u'微软雅黑')
    #字号
    fontSize    = models.IntegerField(default=15)
    #词间距
    #wordSpace   = models.IntegerField(default=5)
    #字符间距
    letterSpace = models.IntegerField(default=1)
    #行高
    lineHeight  = models.IntegerField(default=25)
    #段内距
    paraPadding = models.IntegerField(default=20)
    #是否自动高亮
    hlBackground= models.BooleanField(default=True)
    #背景色
    background  = models.CharField(max_length=8)
    #字色
    fontColor   = models.CharField(max_length=8)
    #高亮字色
    #hlColor     = models.CommaSeparatedIntegerField(default=[88, 88, 88])
    #书签
    chapter     = models.ForeignKey(Chapter, blank=True, null=True, on_delete=models.SET_NULL)
    #等级
    level       = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'reader'
    
class Review(models.Model):
    '''书评'''
    
    #文章名
    subject = models.CharField(max_length=255)
    #作者,一个作者多个书评
    author  = models.ForeignKey(Reader)
    #写作日期
    date  = models.DateTimeField(default=timezone.now())
    #路径
    path    = models.FilePathField()
    #评论的书籍,一本书多个书评
    book    = models.ForeignKey(Book)
    
    class Meta:
        db_table = 'review'
    