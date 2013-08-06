#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from books.utils import save_file_from_request, get_save_folder,\
    Page, ChapterPage, NewChapterException, NoChapterException
from django.contrib.auth.decorators import login_required
from books.models import Book, Chapter
from django.core.exceptions import ObjectDoesNotExist
from edu import settings
from django.http.response import Http404

def Books(request):
    title = u'著作'
    try:
        index = int(request.GET.get('index', 0))
        
        pb = Page(Book, pageLimit=settings.PAGE_ITEM_LIMIT)
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
        chapters = Chapter.objects.order_by('index').filter(book=book)
        first_chapter = chapters[0]
    except ObjectDoesNotExist:
        print "book is not exist"
    return render_to_response('books/chapters.html', locals())

def BookChapter(request, chapterId):
    try:
        chapter = Chapter.objects.get(id=chapterId)
        book = chapter.book
        
        cptPg = ChapterPage(chapterId, get_save_folder())
        lines = cptPg.currentParas()
        request.session['chapter'] = cptPg
    except Exception, e:
        print e
    tip = request.GET.get('tip', '')
    return render_to_response('books/article.html', locals())

def BookChapterNext(request, chapterId):
    try:
        cptPg = request.session['chapter']
        chapter = Chapter.objects.get(id=chapterId)
        book = chapter.book
        lines = cptPg.nextParas()
        request.session['chapter'] = cptPg
        return render_to_response('books/article.html', locals())
    except NewChapterException, e:
        tip = u'后一章节'
        return HttpResponseRedirect('/books/chapter/' + e.args[0] + '?tip=' + tip)
    except NoChapterException, e:
        tip = u'已经是最后一章'
        return HttpResponseRedirect('/books/chapter/' + e.args[0] + '?tip=' + tip)

def BookChapterPrev(request, chapterId):
    try:
        cptPg = request.session['chapter']
        chapter = Chapter.objects.get(id=chapterId)
        book = chapter.book
        lines = cptPg.prevParas()
        request.session['chapter'] = cptPg
    except NewChapterException, e:
        tip = u'前一章节'
        return HttpResponseRedirect('/books/chapter/' + e.args[0] + '?tip=' + tip)
    except NoChapterException, e:
        tip = u'已经是最前一章'
        return HttpResponseRedirect('/books/chapter/' + e.args[0] + '?tip=' + tip)
    
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