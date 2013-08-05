#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from books.utils import save_file_from_request, get_chapters, get_save_folder,\
    Page, ChapterManager
from django.contrib.auth.decorators import login_required
from books.models import Book, Chapter
from django.core.exceptions import ObjectDoesNotExist
from edu import settings

def Books(request):
    title = u'著作'
    try:
        index = int(request.GET.get('index', 0))
        
        pb = Page(Book, settings.PAGE_ITEM_LIMIT)
        counts = range(1, pb.countPage())
        
        if not index or index < 1:
            return HttpResponseRedirect('/books?index=1')
        if index > len(counts):
            return HttpResponseRedirect('/books?index=' + repr(len(counts)))
        
        books = pb.currentPageItems(index)
        reader = request.user.reader
    except Exception, e:
        print e
    return render_to_response('books/books.html', locals())

def Chapters(request, bookId):
    try:
        book = Book.objects.get(id=bookId)
        chapters = ChapterManager(bookId).getChapters()
    except ObjectDoesNotExist:
        print "book is not exist"
    return render_to_response('books/chapters.html', locals())

def BookChapter(request, bookId, chapterId):
    try:
        book = Book.objects.get(id=bookId)
        chapter = Chapter.objects.get(id=chapterId)
        import os
        path = os.path.join(get_save_folder(), repr(book.id))
        lines = ChapterManager(bookId).chapterParas(chapterId, path)
    except Exception, e:
        print e
    return render_to_response('books/article.html', locals())

@login_required
def Share(request):
    title = u'分享书籍'
    if request.method == 'GET':
        nxt = '/'
        return render_to_response('books/share.html', locals())
    else:
        error = {}
        try:
            save_file_from_request(request, 'file')
            error['status'] = True
        except Exception, e:
            error['status'] = False
            error['msg'] = e

        import json
        return HttpResponse(json.dumps(error), 'json')