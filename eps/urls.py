from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ###------------------------------------------------------Paginas:-----------------------------------------------------------###
    #Pagina principal
    url(r'^home','epsapp.views.home',name='home'),

    #Informacion de envio
    url(r'^rastreo','epsapp.views.tracking',name='tracking'),

    ###------------------------------------------------------Empleados:---------------------------------------------------------###
    url(r'^appeps$','epsapp.views.empmain',name='empmain'),                     #Principal empleado
    url(r'^appeps/iniciarsesion$','epsapp.views.emplogin',name='emplogin'),     #Iniciar sesion
    url(r'^appeps/cerrarsesion$','epsapp.views.emplogout',name='emplogout'),    #Cerrar sesion
    
    ###------------------------------------------------------Gerentes--------------------------------------###

    url(r'^appeps/gerente$','epsapp.views.manager',name='manager'),                                                         #Principal gerente
    
    url(r'^appeps/gerente/solicitudes$','epsapp.views.alldelrequest_man',name='alldelrequest_man'),                         #Todas las solicitudes
    url(r'^appeps/gerente/solicitudes/(?P<requestid>\d+)$','epsapp.views.requestdetail_man',name='requestdetail_man'),      #Una solicitud
    url(r'^appeps/gerente/solicitudes/borrar/(?P<requestid>\d+)$','epsapp.views.deletereq',name='deletereq'),               #Borrar solicitud
    url(r'^appeps/gerente/solicitudes/actualizar/(?P<requestid>\d+)$','epsapp.views.updatereq_man',name='updatereq_man'),   #Actualizar solicitud
    
    url(r'^appeps/gerente/buscar$','epsapp.views.searchreq',name='searchreq'),                                              #Buscar solicitud
    
    url(r'^appeps/gerente/facturas$','epsapp.views.bills',name='bills'),                                                    #Lista de facturas
    url(r'^appeps/gerente/facturas/(?P<billid>\d+)$','epsapp.views.billdetail',name='billdetail'),                          #Detalles de una factura
    url(r'^appeps/gerente/reportes$','epsapp.views.reports',name='reports'),                                                #Reportes
    url(r'^appeps/gerente/rutas$','epsapp.views.routes',name='routes'),                                                     #Rutas
    url(r'^appeps/gerente/eventos$','epsapp.views.logs',name='logs'),                                                       #Registro de eventos
    url(r'^appeps/gerente/eventos/filtrar$','epsapp.views.filterlog',name='filterlog'),                                     #Filtrar entradas del log
    url(r'^appeps/gerente/eventos/borrar/(?P<logentryid>\d+)$','epsapp.views.deletelogentry',name='deletelogentry'),        #Eliminar un entrada del log

    ###------------------------------------------------------Empleados--------------------------------------###
    
    url(r'^appeps/despachador$','epsapp.views.dispatcher',name='dispatcher'),                                               #Principal despachador

    url(r'^appeps/despachador/solicitudes$','epsapp.views.alldelrequest_disp',name='alldelrequest_disp'),                   #Todas las solicitudes
    url(r'^appeps/despachador/solicitudes/(?P<requestid>\d+)$','epsapp.views.requestdetail_disp',name='requestdetail_disp'),#Una solicitud
    url(r'^appeps/despachador/solicitudes/borrar/(?P<requestid>\d+)$','epsapp.views.deletereq',name='deletereq'),           #Eliminar solicitud
    url(r'^appeps/despachador/solicitudes/actualizar/(?P<requestid>\d+)$','epsapp.views.updatereq_disp',name='updatereq_disp'), #Actualizar solicitud
    url(r'^appeps/despachador/buscar$','epsapp.views.searchreq',name='searchreq'),                                          #Buscar solicitud
    
    ###------------------------------------------------------Otros--------------------------------------###

    url(r'^appeps/error$','epsapp.views.exception',name='exception'),                                                       #Excepcion o error
    

    ###---Servicios Web:---###

    url(r'^wseps/solicitud$','epsapp.views.wsnewrequest',name='wsnewrequest'),                                             #Crear solicitud
    url(r'^wseps/solicitud/(?P<requestid>VE\d+)$','epsapp.views.wsdetailrequest',name='wsdetailrequest'),                     #Una solicitud
    url(r'^wseps/factura/(?P<billid>\d+)$','epsapp.views.wsdetailbill',name='wsdetailbill'),                     #Una factura

    ###---Administracion:---###
    url(r'^admin/', include(admin.site.urls)),
)
