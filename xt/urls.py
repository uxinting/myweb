from django.conf.urls import patterns, include, url
from xt import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('xt.views',
                       url(r'^$', 'welcome'),
                       url(r'^login/$', 'login'),
                       url(r'^logout/$', 'logout'),
                       url(r'^register/$', 'register'),
                       url(r'^message/$', 'message'),
                       (r'^compositions/', include('xt.composition.urls')),
                       (r'^calligraphys/', include('xt.calligraphy.urls')),
                       (r'^about/', include('xt.about.urls')),
                       (r'^tools/', include('xt.tool.urls')),
    # Examples:
    # url(r'^$', 'xt.views.home', name='home'),
    # url(r'^xt/', include('xt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

mediaurlpatterns = patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                            )

staticurlpatterns = patterns('',
                             (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                             )

urlpatterns += mediaurlpatterns
urlpatterns += staticurlpatterns

