# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Config, Branch
from django.http.response import HttpResponse
import os

CALLIGRAPHYS = 'xt/static/calligraphys'

def contents(request):
    summary = u'常有心于词墨'
    currentpage = 4
    config = Config.objects.all()
    branches = Branch.objects.all()
    title = u'词墨'
    pictures =  os.listdir(CALLIGRAPHYS)[:16]
    return render_to_response('calligraphy/calligraphy.html', locals())

def show(request):
    title = u'词墨'
    pic = request.GET['pic']
    pictures = os.listdir(CALLIGRAPHYS)
    try:
        index = pictures.index(pic)
        if (index <= 0):
            prev = pic
        else:
            prev = pictures[index - 1]
        
        if (index >= len(pictures) - 1):
            nxt = pic
        else:
            nxt = pictures[index + 1]
    except:
        prev = nxt = pic = ""
    
    description = "null"
    return render_to_response('calligraphy/calligraphy-show.html', locals())

def ajax(request):
    if (request.GET['opt'] == 'loadmore'):
        index = int(request.GET['index'])
        if (not index):
            return
        pictures =  os.listdir(CALLIGRAPHYS)[index: index+4]
        return render_to_response('calligraphy/ajax-loadmore.html', locals())
    else:
        return HttpResponse('')