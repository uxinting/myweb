# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config
from django.http.response import HttpResponse, HttpResponseRedirect
import os
from util import ReceiveFile
from xt import settings

def tools(request):
    branches = Branch.objects.all()
    config = Config.objects.all()
    currentpage = 4
    user = request.user
    title = branches.get(id=currentpage).name
    summary = branches.get(id=currentpage).summary
    request.session.set_expiry(0)
    
    return render_to_response('tool/tools.html', locals())

def picture(request):
    try:
        if request.method == "POST":
            ReceiveFile.RemoteFile2(request, 'file', 'picture').receive()
            request.session['picture'] = request.POST['filename']
            return HttpResponseRedirect('/tools')
        return HttpResponse('not post')
    except Exception, e:
        return HttpResponse(e)

def upload(request):
    try:
        if request.method == 'POST':
            file = ReceiveFile.RemoteFile(request).receive()
            
            return HttpResponse('ok' + file)
        return HttpResponse('not post')
    except Exception, e:
        return HttpResponse(e)
    
def ajax(request):
    try:
        if request.method == 'GET':
            type = request.GET['type']
            file = request.session.get(type, 'none')
            path = os.path.join(settings.MEDIA_ROOT, 'file/' + file + '.jpg')
            if file:
                if os.path.isfile(path):
                    return HttpResponse('/media/file/' + file + '.jpg')
                else:
                    return HttpResponse('process')
            else:
                return HttpResponse('')
    except:
        pass