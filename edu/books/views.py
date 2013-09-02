#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from books.utils import save_file_from_request, get_save_folder,\
    Page, ChapterPage, NewChapterException, NoChapterException, createChapter,\
    removeChapter, save_review, read_review, next_chapter, prev_chapter
from django.contrib.auth.decorators import login_required
from books.models import Book, Chapter
from django.core.exceptions import ObjectDoesNotExist
from edu import settings
from django.http.response import Http404
from readers.models import Review

def Books(request):
    title = u'著作'
    try:
        index = int(request.GET.get('index', 0))
        
        pb = Page(Book, pageLimit=settings.PAGE_ITEM_LIMIT)
        counts = [c+1 for c in range(pb.countPage())]
        
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
    except ObjectDoesNotExist:
        print "book is not exist"
    return render_to_response('books/chapters.html', locals())

def Reviews(request, bookId):
    try:
        book = Book.objects.get(id=bookId)
        reviews = Review.objects.order_by('date').filter(book=book)
    except ObjectDoesNotExist:
        print "book is not exist"
    except Exception, e:
        print e
    
    return render_to_response('books/reviews.html', locals())

def BookChapter(request, chapterId):
    try:
        chapter = Chapter.objects.get(id=chapterId)
        import os
        path = os.path.join(chapter.book.path, str(chapter.index)+chapter.subject)
        lines = open(path).readlines()
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/books')
    except Exception, e:
        print e
    tip = request.GET.get('tip', '')
    return render_to_response('books/article.html', locals())

def BookReview(request, reviewId):
    try:
        review = Review.objects.get(id=reviewId)
        lines = read_review(repr(review.id))
    except Exception, e:
        print e
    return render_to_response('books/review.html', locals())

def BookReviewCreate(request, bookId):
    if request.method == 'POST':
        subject = request.POST.get('subject', None)
        content = request.POST.get('content', None)
        
        review = Review.objects.create(subject=subject, author=request.user.reader, book=Book.objects.get(id=bookId))
        review.save();
        save_review(repr(review.id), content)
        return HttpResponse({"msg": "ok"}, 'json');
    return render_to_response('books/review-create.html', locals())

def BookReviewRemove(request):
    return render_to_response('books/review-remove.html', locals())

def BookChapterNext(request, chapterId):
    cid = next_chapter(chapterId)
    if not cid:
        curl = "/books/chapter/" + str(chapterId) + "/?tip=最后一章了"
    else:
        curl = "/books/chapter/" + str(cid)
    return HttpResponseRedirect(curl)

def BookChapterPrev(request, chapterId):
    cid = prev_chapter(chapterId)
    if not cid:
        curl = "/books/chapter/" + str(chapterId) + "/?tip=第一章了"
    else:
        curl = "/books/chapter/" + str(cid)
    return HttpResponseRedirect(curl)

def BookChapterCreate(request):
    try:
        result = {}
        cId = request.POST.get('cId', None)
        cStr = request.POST.get('cStr', None)

        result['msg'] = createChapter(cId, cStr)
    except Exception, e:
        print '+++++++++++++++', e
        result['msg'] = False
    import json
    return HttpResponse(json.dumps(result), 'json')

def BookChapterRemove(request):
    try:
        result = {}
        
        cId = request.POST.get('cId', None)
        cStr = request.POST.get('cStr', None)
        
        result['msg'] = removeChapter(cId, cStr)
    except Exception, e:
        result['msg'] = False
    
    import json
    return HttpResponse(json.dumps(result), 'json')

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