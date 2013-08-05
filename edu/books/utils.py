#-*- coding: utf-8 -*-
import re
import os
from books.models import Book, Chapter
from django.db import models

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
            
        out_f.close()
        return os.path.join(path, repr(book.id))
    except Exception, e:
        raise e

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
    
class ChapterManager:
    '''  chapter options '''
    def __init__(self, bookId):
        self.bookId = bookId
        
    def getChapters(self):
        self.book = Book.objects.get(id=self.bookId)
        return Chapter.objects.order_by('index').filter(book=self.book)
    
    def chapterParas(self, chapterId, bookPath, charLimit=600):
        chapter = Chapter.objects.get(id=chapterId)
        index = chapter.index
        endindex = chapter.endindex
        
        f = open(bookPath)
        f.seek(index)
        if endindex - index < 1000:
            return f.read(endindex - index).split('\n')
        else:
            lines = []
            while True:
                if f.tell()-index > charLimit:
                    break
                line = f.readline()
                if line:
                    lines.append(line)
                else:
                    break
            return lines
        f.close()