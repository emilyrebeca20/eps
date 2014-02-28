from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ###---Paginas:---###
    #Pagina principal
    url(r'^home','epsapp.views.home',name='home'),

    #Informacion de envio
    url(r'^rastreo','epsapp.views.tracking',name='tracking'),

    #Empleados
    url(r'^appeps/login','epsapp.views.emplogin',name='emplogin'),
    url(r'^appeps/logout','epsapp.views.emplogout',name='emplogout'),
    url(r'^appeps/gerente','epsapp.views.manager',name='manager'),
    url(r'^appeps/despachador','epsapp.views.dispatcher',name='dispatcher'),
    url(r'^appeps/error','epsapp.views.exception',name='exception'),
    url(r'^appeps','epsapp.views.empmain',name='empmain'),

    ###---Servicios Web:---###

    ###---Administracion:---###
    url(r'^admin/', include(admin.site.urls)),
)
