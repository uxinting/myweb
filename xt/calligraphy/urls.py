from django.conf.urls import patterns, include, url

urlpatterns = patterns('xt.calligraphy.views',
                       url(r'^$', 'contents'),
                       url(r'^ajax', 'ajax'),
                       url(r'^show', 'show'),
                       )
