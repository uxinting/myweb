#-*- coding: utf-8 -*-
import re
import os
from books.models import Book, Chapter
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

SUBJECT_LEN = 32

def get_save_folder():
    return os.path.join(os.path.dirname(__file__), 'books').decode('gbk')

def get_review_folder():
    return os.path.join(os.path.dirname(__file__), 'reviews').decode('gbk')

def save_review(subject, content):
    path = os.path.join(get_review_folder(), subject)
    try:
        open(path, 'w+').write(content.encode('utf8').replace('<br>', '\n')[:-8])
    except Exception, e:
        print e

def read_review(name):
    return open(os.path.join(get_review_folder(), name)).readlines()

def save_file_from_request(request, name):
    try:
        f = request.FILES.get(name, None)
        book = Book.objects.create(name=''.join(f.name.split('.')[:-1]),
                                   author=request.POST.get('author', 'unknown'),
                                   sharer=request.user,
                                   path='',
                                   desc=request.POST.get('desc', 'no describe'))
        book.save()
        
        temp_path = os.path.join(get_save_folder(), 'temp')
        path = os.path.join(get_save_folder(), repr(book.id))
        
        temp_f = open(temp_path, 'wb+')
        for contents in f.chunks():
            temp_f.write(contents)
                
        #remove blank line
        temp_f.seek(0)
        out_f = open(path, 'w+')
        
        while True:
            line = temp_f.readline()
            if not line:
                break
            if re.compile(r'^\s+$').match(line):
                continue
            out_f.write(line)
        temp_f.close()
        
        #first para as subject
        out_f.seek(0)
        subject = out_f.readline().decode('utf8')[:SUBJECT_LEN]
        
        #size of file
        out_f.seek(0, 2)
        Chapter.objects.create(subject=subject, book=book, index=0, endindex=out_f.tell()).save()
        
        out_f.close()
        return path
    except Exception, e:
        raise e

def createChapter(chapterId, chapterString):
    try:
        book = Chapter.objects.get(id=chapterId).book
        path = os.path.join(get_save_folder(), repr(book.id))
        f = open(path)

        while True:
            line = f.readline()
            
            if not line:
                return False
            if line.startswith(chapterString.encode('utf8')):
                index = f.tell()
                subject = f.readline().decode('utf8')[:SUBJECT_LEN]
                
                #the chapter should be divide
                chapter = Chapter.objects.get(index__lte=index, endindex__gte=index, book=book)
                
                Chapter.objects.create(book=book, subject=subject, index=index, endindex=chapter.endindex).save()
                chapter.endindex = index
                chapter.save()
                return True
            
    except Exception, e:
        print '--------------', e
        return False

def removeChapter(chapterId, chapterString):
    try:
        chapter = Chapter.objects.get(id=chapterId)
        chapterbefore = Chapter.objects.get(endindex=chapter.index)
        
        chapterbefore.endindex = chapter.endindex
        chapterbefore.save()
        
        chapter.delete()
    except Exception, e:
        print '----------------', e
        return False

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
    def __init__(self, chapterId, dirPath, **args):
        self.id = chapterId
        self.path = os.path.join(dirPath, repr(Chapter.objects.get(id=self.id).book.id))
        self.limit = args.get('pageLimit', -1)
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
        if self.limit == -1 or self.endindex - self.index < self.limit*3*2:#两倍之内，直接显示
            book.seek(self.index)
            lines = []
            
            while True:
                lines.append(book.readline())
                if book.tell() >= self.endindex:
                    break
                
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
