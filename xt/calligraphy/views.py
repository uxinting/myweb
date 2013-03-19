# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Config, Branch
from django.http.response import HttpResponse
import os

CALLIGRAPHYS = os.path.join(os.path.dirname(__file__), 'calligraphys')

def contents(request):
    summary = u'常有心于词墨'
    currentpage = 4
    config = Config.objects.all()
    branches = Branch.objects.all()
    title = u'词墨'
    return render_to_response('calligraphy/calligraphy.html', locals())

def ajax(request):
    class PIC():
        name = ''
        style = ''
    if (request.GET['opt'] == 'loadmore'):
        pictures = os.listdir(CALLIGRAPHYS)
        return render_to_response('calligraphy/ajax-loadmore.html', locals())
    else:
        return HttpResponse('')