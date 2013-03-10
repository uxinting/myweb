from django.conf.urls import patterns, include, url

urlpatterns = patterns('xt.composition.views',
                       url(r'^$', 'contents'),
                       url(r'^show/(?P<index>\d+)$', 'show'),
                       url(r'^create/$', 'create'),
                       )
