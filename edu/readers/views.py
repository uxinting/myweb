#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from readers.models import Reader
from django.shortcuts import render_to_response

@login_required
def Config(request):
    error = {}
    if request.method == 'GET':
        title = u'个人设置'
        return render_to_response('readers/config.html', locals())
    else:
        try:
            reader = Reader.objects.get_or_create(user=request.user)
            for k,v in request.POST.items():
                print k,v
                if hasattr(reader[0], k) and v:
                    setattr(reader[0], k, v)
            print reader
            reader[0].save()
            error['msg'] = u'保存成功'
        except Exception, e:
            error['msg'] = e
        return HttpResponse(error['msg'], 'text/plain')