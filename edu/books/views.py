#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from books.utils import save_file_from_request, get_chapters
from django.contrib.auth.decorators import login_required
from books.models import Book

def Books(request):
    title = u'著作'
    try:
        index = request.GET.get('index', None)
        if not index:
            return HttpResponseRedirect('/?index=0')
        
        index = int(index)
        option = request.GET.get('option', None)
        if option == 'prev':
            index = index - 10
            if index < 0:
                index = 0;
        elif option == 'next':
            index = index + 10
        else:pass

        books = Book.objects.all()[index : index+10]
        reader = request.user.reader
    except Exception, e:
        print e
    return render_to_response('books/books.html', locals())

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
        print error
        import json
        return HttpResponse(json.dumps(error), 'json')