from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ###---Paginas:---###
    #Pagina principal
    url(r'^home','epsapp.views.home',name='home'),

    #Informacion de envio
    url(r'^rastreo','epsapp.views.tracking',name='tracking'),

    ###---Servicios Web:---###

    ###---Administracion:---###
    url(r'^admin/', include(admin.site.urls)),
)
