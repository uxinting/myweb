from django.conf.urls import patterns, url

urlpatterns = patterns('readers.views',
                       url(r'config', 'Config'),
                       )