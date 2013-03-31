# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config
from django.conf import settings
from django.http.response import HttpResponse
import os

def tools(request):
    title = u'以用'
    summary = u'以利器善公之事'
    branches = Branch.objects.all()
    config = Config.objects.all()
    currentpage = 4
    return render_to_response('tool/tools.html', locals())

def upload(request):
    try:
        if request.method == 'POST':
            file = request.FILES.get('file', '')
            filename = file.name
            
            fname = os.path.join(settings.MEDIA_ROOT, 'file/', filename)
            if os.path.exists(fname):
                os.remove(fname)
            dirs = os.path.dirname(fname)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
                
            fp = open(fname, 'wb')
            for content in file.chunks():
                fp.write(content)
            fp.close()
            
            return HttpResponse('ok' + filename + ' ' + fname)
        return HttpResponse('not post')
    except Exception, e:
        return HttpResponse(e)