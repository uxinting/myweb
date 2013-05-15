#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import os
from xinting import settings

CALLIGRAPHY = os.path.join(settings.STATIC_ROOT, 'calligraphy')

def calligraphy(request):
    title = u'calligraphy'
    calligraphys = os.listdir(CALLIGRAPHY)
    return render_to_response('calligraphy/calligraphy.html', locals())