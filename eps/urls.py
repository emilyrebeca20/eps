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
    url(r'^appeps$','epsapp.views.empmain',name='empmain'),
    url(r'^appeps/iniciarsesion$','epsapp.views.emplogin',name='emplogin'),
    url(r'^appeps/cerrarsesion$','epsapp.views.emplogout',name='emplogout'),
    
    url(r'^appeps/gerente$','epsapp.views.manager',name='manager'),
    url(r'^appeps/gerente/solicitudes$','epsapp.views.alldelrequest_man',name='alldelrequest_man'),
    url(r'^appeps/gerente/solicitudes/(?P<requestid>\d+)$','epsapp.views.requestdetail_man',name='requestdetail_man'),
    url(r'^appeps/gerente/solicitudes/borrar/(?P<requestid>\d+)$','epsapp.views.deletereq',name='deletereq'),
    url(r'^appeps/gerente/buscar$','epsapp.views.searchreq',name='searchreq'),
    url(r'^appeps/gerente/reportes$','epsapp.views.reports',name='reports'),
    url(r'^appeps/gerente/eventos$','epsapp.views.logs',name='logs'),
    
    url(r'^appeps/despachador$','epsapp.views.dispatcher',name='dispatcher'),
    url(r'^appeps/despachador/solicitudes$','epsapp.views.alldelrequest_disp',name='alldelrequest_disp'),
    url(r'^appeps/despachador/solicitudes/(?P<requestid>\d+)$','epsapp.views.requestdetail_disp',name='requestdetail_disp'),
    url(r'^appeps/despachador/solicitudes/borrar/(?P<requestid>\d+)$','epsapp.views.deletereq',name='deletereq'),
    url(r'^appeps/despachador/buscar$','epsapp.views.searchreq',name='searchreq'),
    
    url(r'^appeps/error$','epsapp.views.exception',name='exception'),
    

    ###---Servicios Web:---###

    ###---Administracion:---###
    url(r'^admin/', include(admin.site.urls)),
)
