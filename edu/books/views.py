#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from readers.models import Reader

def Books(request):
    title = u'著作'
    try:
        user = request.user
        reader = user.reader
    except:
        pass
    return render_to_response('books/books.html', locals())