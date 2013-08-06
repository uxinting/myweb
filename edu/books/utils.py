#-*- coding: utf-8 -*-
import re
import os
from books.models import Book, Chapter
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

def get_save_folder():
    return os.path.join(os.path.dirname(__file__), 'books').decode('gbk')

def save_file_from_request(request, name):
    try:
        f = request.FILES.get(name, None)
        path = get_save_folder()
        book = Book.objects.create(name=''.join(f.name.split('.')[:-1]),
                                   author=request.POST.get('author', 'unknown'),
                                   sharer=request.user,
                                   path=path,
                                   desc=request.POST.get('desc', 'no describe'))
        book.save()
        out_f = open(os.path.join(path, repr(book.id)), 'wb')
        for content in f.chunks():
            out_f.write(content)
        
        Chapter.objects.create(subject=out_f.readline()[:61], book=book, index=0, endindex=out_f.tell()).save()
        out_f.close()
        return os.path.join(path, repr(book.id))
    except Exception, e:
        raise e

def removeBlankPara(path):
    f = open(path)
    lines = []
    for line in f.readlines():
        if line == '\n':
            continue
        lines.append(line)
    f.close()
    f = open(path, 'w')
    for line in lines:
        f.write(line)
    f.close()

class Page:
    ''' sliced models into pages '''
    def __init__(self, obj, pageLimit=10):
        if not issubclass(obj, models.Model):
            raise TypeError('Model object only!')
        self.model = obj
        self.limit = pageLimit
        try:
            self.count = self.model.objects.count() / self.limit + 1
        except Exception, e:
            raise e
        
    def countPage(self):
        ''' return the count of pages while each one contain self.limit model items '''
        return self.count
        
    def currentPageItems(self, page):
        ''' get items in page 'page', index base of 1 '''
        if page > self.count:
            page = self.count
        if page < 1:
            page = 1;
        try:
            page *= self.limit
            return self.model.objects.all()[page-self.limit: page]
        except Exception, e:
            raise e
        
    def prevPageItems(self, page):
        ''' get items in previous page of 'page' '''
        page -= 1
        if page < 1 or page > self.count:
            return None
        return self.currentPageItems(page)
    
    def nextPageItems(self, page):
        ''' get items in next page of 'page' '''
        page += 1
        if page < 1 or page > self.count:
            return None
        return self.currentPageItems(page)

class NewChapterException(Exception):
    pass

class NoChapterException(Exception):
    pass

class ChapterPage:
    ''' chapter pages '''
    def __init__(self, chapterId, dirPath, pageLimit=600):
        self.id = chapterId
        self.path = os.path.join(dirPath, repr(Chapter.objects.get(id=self.id).book.id))
        self.limit = pageLimit
        self.previndex = []
        self.index = None
        self.book = None
        
    def setId(self, chapterId):
        self.id = chapterId
    
    def getId(self):
        return self.id
    
    def currentParas(self):
        if self.index is None:
            chapter = Chapter.objects.get(id=self.id)
            self.index = chapter.index
            self.endindex = chapter.endindex
            self.book = chapter.book
            
        book = open(self.path)
        self.previndex.append(self.index)
        print self.previndex
        if self.endindex != -1 and self.endindex - self.index < self.limit*3*2:#两倍之内，直接显示
            book.seek(self.index)
            lines = book.read(self.endindex-self.index-1).split('\n')
            self.index = book.tell()
            book.close()
            return lines
        else:
            book.seek(self.index)
            c = 0
            lines = []
            while c < self.limit:
                line = book.readline()
                c += len(line.decode('utf8'))
                lines.append(line)
            
            self.index = book.tell()
            book.close()
            return lines
        
    def prevParas(self):
        if self.previndex is None:
            return None
        try:
            self.previndex.pop()
            self.index = self.previndex.pop()
        except:#没有前一页,到前一章
            index = Chapter.objects.get(id=self.id).index
            try:
                prevc = Chapter.objects.get(endindex=index, book=self.book)
            except ObjectDoesNotExist:
                raise NoChapterException(self.id)
            raise NewChapterException(prevc.id)
        
        return self.currentParas()
    
    def nextParas(self):
        if self.index >= self.endindex and self.endindex != -1:
            try:
                nextc = Chapter.objects.get(index=self.endindex, book=self.book)
                raise NewChapterException(nextc.id)
            except ObjectDoesNotExist:
                raise NoChapterException(self.id)
        
        return self.currentParas()
    
        
class ChapterManager:
    '''  chapter options '''
    def __init__(self, bookId):
        self.bookId = bookId
        
    def getChapters(self):
        self.book = Book.objects.get(id=self.bookId)
        return Chapter.objects.order_by('index').filter(book=self.book)
    
    def chapterParas(self, chapterId, bookPath, charLimit=1600):
        chapter = Chapter.objects.get(id=chapterId)
        index = chapter.index
        endindex = chapter.endindex
        
        f = open(bookPath)
        f.seek(index)
        if endindex - index < 1000 and endindex != -1:
            return f.read(endindex - index).split('\n')
        else:
            lines = []
            number = 0;
            while True:
                if number-index > charLimit:
                    break
                line = f.readline()
                number += len(line.decode('utf8'))
                if line or line == '\n':
                    lines.append(line)
                else:
                    print f.tell(), 'break'
                    break
            return lines
        f.close()
        
    def nextParas(self):
        pass