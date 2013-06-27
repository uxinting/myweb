#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from books.utils import save_file_from_request, get_chapters
from django.contrib.auth.decorators import login_required

def Books(request):
    title = u'著作'
    try:
        reader = request.user.reader
    except:
        pass
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
            fpath = save_file_from_request(request, 'file')
            error['msg'] = get_chapters(request.POST.get('rule', '^$'), open(fpath).readlines())
            error['status'] = True
        except Exception, e:
            print e
            error['status'] = False
            error['msg'] = e
        import json
        return HttpResponse(json.dumps(error), 'json')