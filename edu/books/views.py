#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def Books(request):
    title = u'著作'
    user = request.user
    return render_to_response('edu/books.html', locals())