#-*- coding: utf-8 -*-
import re
import os
from books.models import Book

def get_save_folder():
    return os.path.join(os.path.dirname(__file__), 'books') 

def save_file_from_request(request, name):
    try:
        f = request.FILES.get(name, None)
        path = get_save_folder()
        book = Book.objects.create(name=''.join(f.name.split('.')[:-1]),
                                   author=request.POST.get('author', 'unknown'),
                                   sharer=request.user,
                                   path=path,
                                   desc=request.POST.get('desc', f.chunks()[:100]))
        book.save()
        out_f = open(os.path.join(path, repr(book.id)), 'wb')
        for content in f.chunks():
            out_f.write(content)
            
        out_f.close()
        return os.path.join(path, repr(book.id))
    except Exception, e:
        raise e

def get_chapters(rule, lines):
    chapters = []
    c_r = re.compile(rule)
    for line in lines:
        line = line.decode('utf-8')
        if re.match(c_r, line):
            chapters.append(line)
    return chapters