#-*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from books.utils import get_save_folder, Page, ChapterPage,\
    NoChapterException, createChapter
import os
from books.models import Book, Chapter
from django.db import models


'''class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    def test_get_chapters(self):
        path = os.path.join(get_save_folder(), '4L')
        get_chapters(u'.*篇第.+', open(path).readlines())
        '''
#print get_save_folder().decode('gbk')    
#print Page(Book).currentPageItems(1)
#for c in ChapterManager(1).getChapters():
#    print c.subject
''''c = ChapterPage(3, get_save_folder())
for para in c.currentParas():
    print para
    
for para in c.nextParas():
    print para
    
for para in c.prevParas():
    print para''''''
try:
    raise NoChapterException(1)
except NoChapterException, e:
    print e.args'''
createChapter(9, u'卷第一')