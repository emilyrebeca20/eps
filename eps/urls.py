from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^template','epsapp.views.templatet',name='templatet'),

    url(r'^admin/', include(admin.site.urls)),
)
