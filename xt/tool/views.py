# _*_ coding: gb2312 _*_
from django.shortcuts import render_to_response
from xt.models import Branch, Config
from django.conf import settings
from django.http.response import HttpResponse
import os
from util import ReceiveFile

def tools(request):
    branches = Branch.objects.all()
    config = Config.objects.all()
    currentpage = 4
    user = request.user
    title = branches.get(id=currentpage).name
    summary = branches.get(id=currentpage).summary
    return render_to_response('tool/tools.html', locals())

def picture(request):
    try:
        if request.method == "POST":
            ReceiveFile.RemoteFile2(request, 'file', 'picture').receive()
            return HttpResponse('ok')
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