# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Config, Branch
from django.http.response import HttpResponse
import os

CALLIGRAPHYS = 'xt/static/calligraphys'

class PicInfo():
    name = ''
    style = ''
    
def contents(request):
    summary = u'常有心于词墨'
    currentpage = 4
    config = Config.objects.all()
    branches = Branch.objects.all()
    title = u'词墨'
    pictures = []
    for pic in os.listdir(CALLIGRAPHYS)[:16]:
        #import Image
        #image = Image.open(os.path.join(CALLIGRAPHYS, pic))
        p = PicInfo()
        p.name = pic
        p.style = 'width: 280px'
        #p.style = image.size[0] > image.size[1] and 'width: ' + repr(image.size[0]) + 'px' or 'height: ' + repr(image.size[1]) + 'px'
        pictures.append(p)
    return render_to_response('calligraphy/calligraphy.html', locals())

def ajax(request):
    pictures = []
    if (request.GET['opt'] == 'loadmore'):
        index = int(request.GET['index'])
        if (not index):
            return
        for pic in os.listdir(CALLIGRAPHYS)[index: index+4]:
            #import Image
            #image = Image.open(os.path.join(CALLIGRAPHYS), f)
            p = PicInfo()
            p.name = pic
            p.style = 'width: 280px'
            #pic.style = image.size[0] > image.size[1] and 'width: ' + image.size[0] or 'height: ' + image.size[1]
            pictures.append(p)
        return render_to_response('calligraphy/ajax-loadmore.html', locals())
    else:
        return HttpResponse('')