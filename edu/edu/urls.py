from django.conf.urls import patterns, include, url
from edu import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^accounts', include('accounts.urls')),
                       url(r'^$', 'books.views.Books'),
                       (r'^books', include('books.urls')),
    # Examples:
    # url(r'^$', 'edu.views.home', name='home'),
    # url(r'^edu/', include('edu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)