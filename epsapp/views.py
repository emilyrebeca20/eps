# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import *
from datetime import *
from epsapp.models import *
from epsapp.decorators import *
from epsapp.forms import *
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import *
from django.template import RequestContext,Context
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
import StringIO
import random
from datetime import timedelta, date, datetime
from django.utils.timezone import *
from pytz import timezone
import pytz
from django.db import transaction
import requests


# Create your views here.

#Renderiza la plantilla padre
def home(request):
	return render(request,'home.html')

#Consulta de solicitud por numero de rastreo
def tracking(request):
	if request.method == 'GET':
		params = request.GET 
		if 'trackingn' in params:
			trackingnum = params['trackingn']
			delivery_req = DeliveryRequest.objects.filter(tracking_number=trackingnum)
			if delivery_req.count() == 1:
				return render(request,'trackinginfo.html',{'deliveryreq':delivery_req.first()})
			else:
				messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
				return render(request,'trackinginfo.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Pantalla principal de empleados
def empmain(request):
	return render(request,'empmain.html')

#Inicio de sesion de empleados
def emplogin(request):
	#print 'Hola'
	if request.method == 'POST':
		params = request.POST
		if 'username' in params and 'password' in params:
			user = authenticate(username=params['username'], password=params['password'])
			if user is not None:
				if user.is_active:
					profile = Employee.objects.filter(user=user)
					if profile.count() == 1:
						login(request,user)
						messages.success(request,'Inicio de sesión exitoso.',extra_tags='success')
						
						mssg = u'El empleado ' + user.first_name + ' ' + user.last_name + u' ha iniciado sesión en el sistema.'
						newlogentry = LogEntry(
							event_type='EMP',
							event_desc=mssg)
						newlogentry.save()

						if profile.first().role.role_name == 'Gerente':
							return HttpResponseRedirect('/appeps/gerente')
						elif profile.first().role.role_name == 'Despachador':
							return HttpResponseRedirect('/appeps/despachador')
						else:
							messages.warning(request,'No tiene rol asignado.',extra_tags='warning')
							return HttpResponseRedirect('/appeps')
					else:
						messages.warning(request,'No es empleado.',extra_tags='warning')
						return HttpResponseRedirect('/appeps')
				else:
					messages.error(request,'Esta cuenta ha sido deshabilitada.',extra_tags='danger')
					return HttpResponseRedirect('/appeps')
			else:
				messages.error(request,'El nombre de usuario y/o contraseña es incorrecto.',extra_tags='danger')
				return HttpResponseRedirect('/appeps')
		else:
			messages.error(request,'Parametros incompletos.',extra_tags='danger')
			return HttpResponseRedirect('/appeps')
	else:
		return HttpResponse(status=400)

#Pantalla principal del gerente
@manager_required
def manager(request):
	return render(request,'managermain.html')

#Pantalla principal del despachador
@employee_required
def dispatcher(request):
	return render(request,'employeemain.html')

#Todas las solicitudes de envio (despachador)
@employee_required
def alldelrequest_disp(request):
	delrequests = DeliveryRequest.objects.all()
	if delrequests.count() <= 0:
		messages.warning(request,'No existen solicitudes registradas en el sistema.',extra_tags='warning')
	return render(request,'deliveryrequest-disp.html',{'delrequests':delrequests})

#Todas las solicitudes de envio (gerente)
@manager_required
def alldelrequest_man(request):
	delrequests = DeliveryRequest.objects.all()
	if delrequests.count() <= 0:
		messages.warning(request,'No existen solicitudes registradas en el sistema.',extra_tags='warning')
	return render(request,'deliveryrequest-man.html',{'delrequests':delrequests})

#Detalle de solicitud de envio (despachador)
@employee_required
def requestdetail_disp(request,requestid):
	if request.method == 'GET':
		if requestid:
			delivery_req = DeliveryRequest.objects.filter(id=requestid)
			if delivery_req.count() == 1:
				return render(request,'deliveryrequest-detail-disp.html',{'deliveryreq':delivery_req.first()})
			else:
				messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
				return render(request,'deliveryrequest-detail-disp.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Detalle de solicitud de envio (gerente)
@manager_required
def requestdetail_man(request,requestid):
	if request.method == 'GET':
		if requestid:
			delivery_req = DeliveryRequest.objects.filter(id=requestid)
			if delivery_req.count() == 1:
				return render(request,'deliveryrequest-detail-man.html',{'deliveryreq':delivery_req.first()})
			else:
				messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
				return render(request,'deliveryrequest-detail-man.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Actualizar el estado de una solicitud de envío
@manager_required
def updatereq_man(request,requestid):
	delivery_req = DeliveryRequest.objects.filter(id=requestid)
	if delivery_req.count() == 1:
		if request.method == 'POST': # If the form has been submitted...
			form = UpdateStatusForm(request.POST) # A form bound to the POST data
			if form.is_valid(): # All validation rules pass
				# Process the data in form.cleaned_data
				# ...
				status = form.cleaned_data['status']
				location = form.cleaned_data['location']
				newstatus = Status(
					status=status,
					location=location,
					delrequest=delivery_req.first())
				newstatus.save()

				messages.success(request,'La solicitud ha sido actualizada exitosamente.',extra_tags='success')
				return HttpResponseRedirect('/appeps/gerente/solicitudes/'+str(requestid))
		else:
			form = UpdateStatusForm() # An unbound form

		return render(request,'deliveryrequest-update-man.html', {
			'form': form,
			#'requestid':requestid,
			'deliveryreq':delivery_req.first(),
		})
	else:
		messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
		return render(request,'deliveryrequest-update-man.html')

@employee_required
def updatereq_disp(request,requestid):
	delivery_req = DeliveryRequest.objects.filter(id=requestid)
	if delivery_req.count() == 1:
		if request.method == 'POST': # If the form has been submitted...
			form = UpdateStatusForm(request.POST) # A form bound to the POST data
			if form.is_valid(): # All validation rules pass
				# Process the data in form.cleaned_data
				# ...
				status = form.cleaned_data['status']
				location = form.cleaned_data['location']
				newstatus = Status(
					status=status,
					location=location,
					delrequest=delivery_req.first())
				newstatus.save()

				messages.success(request,'La solicitud ha sido actualizada exitosamente.',extra_tags='success')
				return HttpResponseRedirect('/appeps/despachador/solicitudes/'+str(requestid))
		else:
			form = UpdateStatusForm() # An unbound form

		return render(request,'deliveryrequest-update-disp.html', {
			'form': form,
			#'requestid':requestid,
			'deliveryreq':delivery_req.first(),
		})
	else:
		messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
		return render(request,'deliveryrequest-update-disp.html')

#Eliminar una solicitud de envio
@employee_required
def deletereq(request,requestid):
	if request.method == 'GET':
		if requestid:
			delivery_req = DeliveryRequest.objects.filter(id=requestid)
			if delivery_req.count() == 1:
				user = request.user
				first_name = user.first_name
				last_name = user.last_name

				tracking_number = delivery_req.first().tracking_number
				delivery_req.first().delete()
				messages.success(request,'La solicitud ha sido eliminada.',extra_tags='success')
				
				#Registrar evento	
				mssg = u'El empleado ' + user.first_name + ' ' + user.last_name + u' ha eliminado la solicitud.' + ' ' + tracking_number
				newlogentry = LogEntry(
					event_type='REQ',
					event_desc=mssg)
				newlogentry.save()

				return HttpResponseRedirect('/appeps/gerente/solicitudes')
			else:
				messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
				return render(request,'errtemplate.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Buscar una solicitud de envio por numero de rastreo
@employee_required
def searchreq(request):
	if request.method == 'GET':
		requser = request.user 
		userobjs = User.objects.filter(id=requser.id)
		userobj = userobjs.first()
		profile = Employee.objects.filter(user=userobj)
		userprof = profile.first()
		params = request.GET 
		if 'searchitem' in params:
			trackingnum = params['searchitem']
			delivery_req = DeliveryRequest.objects.filter(tracking_number=trackingnum)
			if delivery_req.count() == 1:	
				if userprof.role.role_name == 'Gerente':
					return render(request,'deliveryrequest-detail-man.html',{'deliveryreq':delivery_req.first()})
				elif userprof.role.role_name == 'Despachador':
					return render(request,'deliveryrequest-detail-disp.html',{'deliveryreq':delivery_req.first()})
				else:
					return HttpResponse(status=400)
			else:
				if userprof.role.role_name == 'Gerente':
					messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
					return render(request,'deliveryrequest-detail-man.html')
				elif userprof.role.role_name == 'Despachador':
					messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
					return render(request,'deliveryrequest-detail-disp.html')
				else:
					return HttpResponse(status=400)
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Lista de facturas
@manager_required
def bills(request):
	if request.method == 'GET':
		bills = Bill.objects.all()
		if bills.count() <= 0:
			messages.warning(request,'No existen facturas registradas en el sistema.',extra_tags='warning')
		return render(request,'bills-man.html',{'bills':bills})
	else:
		return HttpResponse(status=400)

#Detalle de factura
@manager_required
def billdetail(request,billid):
	if request.method == 'GET':
		if billid:
			bills = Bill.objects.filter(id=billid)
			if bills.count() == 1:
				bill = bills.first()
				return render(request,'bills-detail-man.html',{'bill':bill})
			else:
				messages.error(request,'La factura requerida no existe.',extra_tags='danger')
				return render(request,'bills-detail-man.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Listado de rutas
@manager_required
def routes(request):
	return render(request,'routes-man.html')

#Todos los Reportes
@manager_required
def reports(request):
	reports = Report.objects.all()
	form = CreateReportForm()
	messages.success(request,'Principal reportes.',extra_tags='success')
	return render(request,'reports-man.html',{'reports':reports,'form':form})

#Crear reporte
@manager_required
def newreport(request):
	if request.method == 'POST':
		form = CreateReportForm(request.POST)
		if form.is_valid():
			cdata = form.cleaned_data
			#int_init = datetime.strptime(str(cdata['int_init']),'%d/%m/%Y %H:%M:%S')
			#int_end = datetime.strptime(str(cdata['int_end']),'%d/%m/%Y %H:%M:%S')
			type = cdata['type']
			int_init = cdata['int_init']
			int_end = cdata['int_end']
			print int_init
			print int_end
			print type
			employee = request.user.employee

			#employee
			newreport = Report(int_init=int_init,int_end=int_end,type=type,employee=employee)
			newreport.save()
			print newreport
			messages.success(request,'Formulario de nuevo reporte válido.\nReporte creado',extra_tags='success')
			return HttpResponseRedirect('/appeps/gerente/reportes/'+str(newreport.id))
		else:
			messages.error(request,'Formulario de nuevo reporte inválido',extra_tags='danger')
			return HttpResponseRedirect('/appeps/gerente/reportes')
	else:
		form = CreateReportForm()
		messages.success(request,'Nuevo reporte.',extra_tags='success')
		return render(request,'reports-man.html',{'form':forms})

#Detalles reporte
@manager_required
def reportdetail(request,reportid):
	reports = Report.objects.filter(id=reportid)
	if reports.count():
		report = reports.first()
		int_init = report.int_init
		int_end = report.int_end
		type = report.type
		if type == '01':
			msg = 'Solicitudes despachadas y tiempo de despacho'
			#Solicitudes despachadas, el intervalo indicado se aplica a la fecha en que fueron despachadas (no funciona bien)
			reportquery = DeliveryRequest.objects.filter(status__status='02',status__status_date__range=(int_init,int_end))
		elif type == '02':
			msg = 'Solicitudes pendientes y tiempo pendiente'
			#Solicitudes pendientes y tiempo pendiente, el intervalo indicado se aplica a la fecha en que fueron creadas
			reportquery = DeliveryRequest.objects.filter(request_date__range=(int_init,int_end)).exclude(status__status='02').exclude(status__status='03')
		elif type == '03':
			msg = 'Clientes ordenados por cantidad de solicitudes'
			deliveryreq = DeliveryRequest.objects.filter(request_date__range=(int_init,int_end))
			reportquery = Associated.objects.filter()
		elif type == '04':
			msg = 'Destinos ordenados por cantidad de solicitudes'
			#Destinos ordenados por cantidad de solicitudes, el intervalo indicado se aplica a la fecha de las solicitudes
			deliveryreq = DeliveryRequest.objects.filter(request_date__range=(int_init,int_end))
			for dr in deliveryreq:
			reportquery = Location.objects.all()
		elif type == '05':
			msg = 'Facturas ordenadas por tiempo de cancelacion'
			#Facturas ordenadas por tiempo de cancelacion, el intervalo se aplica a la fecha de cancelacion de la factura
			reportquery = Bill.objects.filter(payment_date__range=(int_init,int_end))
		elif type == '06':
			msg = 'Facturas vigentes por cobrar'
			#Facturas vigentes por cobrar, el intervalo indicado se aplica a la fecha de creacion de la factura
			reportquery = Bill.objects.filter(issuance_date__range=(int_init,int_end),payment_status='00')
		elif type == '07':
			msg = 'Facturas vencidas por cobrar'
			#Facturas vencidas por cobrar, el intervalo indicado se aplica a la fecha de creacion de la factura
			reportquery = Bill.objects.filter(issuance_date__range=(int_init,int_end),payment_status='02')

		messages.success(request,'Detalle de reporte.',extra_tags='success')
		return render(request,'reports-detail-man.html',{'report':report,'msg':msg,'reportquery':reportquery})
	else:
		messages.error(request,'No se encontró el reporte.',extra_tags='danger')
		return render(request,'reports-detail-man.html')

#Registro de eventos
@manager_required
def logs(request):
	logentrys = LogEntry.objects.all()
	return render(request,'logs-man.html',{'logentrys':logentrys})

#Filtrado del registro de eventos
@manager_required
def filterlog(request):
	if request.method == 'GET':
		params = request.GET
		if 'idateinterval' in params and 'itimeinterval' in params and 'edateinterval' in params and 'etimeinterval' in params and 'entrytype' in params:
			idateinterval = params['idateinterval']
			itimeinterval = params['itimeinterval']
			edateinterval = params['edateinterval']
			etimeinterval = params['etimeinterval']
			entrytype = params['entrytype']
			initi = idateinterval + ' ' + itimeinterval
			endi = edateinterval + ' ' + etimeinterval
			finiti = datetime.strptime(initi,'%d/%m/%Y %H:%M:%S')
			fendi = datetime.strptime(endi,'%d/%m/%Y %H:%M:%S')
			if entrytype == 'ALL':
				logentrys = LogEntry.objects.filter(event_date__range=(finiti,fendi))
			else:
				logentrys = LogEntry.objects.filter(event_date__range=(finiti,fendi)).filter(event_type=entrytype)
			return render(request,'logs-man.html',{'logentrys':logentrys})
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#Cierre de sesion
@employee_required
def emplogout(request):
	user = request.user
	first_name = user.first_name
	last_name = user.last_name
	logout(request)
	messages.success(request,'Cierre de sesión exitoso.',extra_tags='success')

	mssg = u'El empleado ' + first_name + ' ' + last_name + u' ha cerrado sesión en el sistema.'
	newlogentry = LogEntry(
		event_type='EMP',
		event_desc=mssg)
	newlogentry.save()

	return HttpResponseRedirect('/appeps')

#Excepciones
def exception(request):
	render(request,'errtemplate.html')

#Cruds

#Eliminar una entrada del registro
@manager_required
def deletelogentry(request,logentryid):
	if request.method == 'GET':
		if logentryid:
			logentry = LogEntry.objects.filter(id=logentryid)
			if logentry.count() == 1:
				logentry.first().delete()
				messages.success(request,'La entrada del registro ha sido eliminada.',extra_tags='success')
				return HttpResponseRedirect('/appeps/gerente/eventos')
			else:
				messages.error(request,'El registro solicitado no existe.',extra_tags='danger')
				return render(request,'errtemplate.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

#------------------------------------------------------------------Servicios Web---------------------------------------------------------#
#Genera un xml a partir de la factura
def xmlbill(billreq):
	try:
		delreqbill = Bill.objects.get(pk=billreq)
	except Bill.DoesNotExist:
		print 'No existe la factura o la solicitud de envio'
	except MultipleObjectsReturned:
		print 'Existen varias facturas que coiniciden con la solicitud de envio'
	else:
		delreq = delreqbill.request
		#print 'Factura: ' + str(delreqbill)
		factura = etree.Element('factura')
		etree.SubElement(factura,'idFactura').text = str(delreqbill.pk)
		actores = etree.SubElement(factura,'actores')
		emisor = etree.SubElement(actores,'emisor')
		etree.SubElement(emisor,'rifEmisor').text = str(delreqbill.dist_rif)
		etree.SubElement(emisor,'nombreEmisor').text = str(delreqbill.dist_name)
		etree.SubElement(emisor,'cuenta').text = str(delreqbill.account_number)
		pagador = etree.SubElement(actores,'pagador')
		etree.SubElement(pagador,'rifPagador').text = str(delreq.associated_comm.rif)
		etree.SubElement(pagador,'nombrePagador').text = str(delreq.associated_comm.assoc_name)
		despachos = etree.SubElement(factura,'despachos')
		despacho = etree.SubElement(despachos,'despacho')
		productos = etree.SubElement(despacho,'productos')
		packagelist = delreq.package_set.all()
		for packageunit in packagelist:
			producto = etree.SubElement(productos,'producto')
			etree.SubElement(producto,'id').text = str(packageunit.pk)
			etree.SubElement(producto,'nombre').text = str(packageunit.description)
			etree.SubElement(producto,'cantidad').text = str(packageunit.amount)
			medidas = etree.SubElement(producto,'medidas')
			etree.SubElement(medidas,'peso').text = str(packageunit.weigth)
			etree.SubElement(medidas,'largo').text = str(packageunit.length)
			etree.SubElement(medidas,'ancho').text = str(packageunit.width)
			etree.SubElement(medidas,'alto').text = str(packageunit.height)
			#print packageunit
		etree.SubElement(despacho,'tracking').text = str(delreq.tracking_number)
		etree.SubElement(despacho,'costo').text = str(delreqbill.total)
		costos = etree.SubElement(factura,'costos')
		etree.SubElement(costos,'subtotal').text = str(delreqbill.sub_total)
		etree.SubElement(costos,'impuestos').text = str(delreqbill.taxes)
		etree.SubElement(costos,'total').text = str(delreqbill.total)

		fechas = etree.SubElement(factura,'fechas')
		etree.SubElement(fechas,'fechaEmision').text = str(delreqbill.issuance_date.astimezone(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M'))
		etree.SubElement(fechas,'fechaVencimiento').text = str(delreqbill.expiration_date.astimezone(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M'))
		if delreqbill.payment_date:
			paymentdate = delreqbill.payment_date.astimezone(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M')
		else:
			paymentdate = delreqbill.payment_date
		etree.SubElement(fechas,'fechaPago').text = str(paymentdate)

		statuses = etree.SubElement(factura,'statuses')
		statuslist = delreq.status_set.all()
		for statusunit in statuslist:
			date = statusunit.status_date.astimezone(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M')
			if statusunit.status == '00':
				stat = 'Recibido'
			elif statusunit.status == '01':
				stat = 'Por despachar'
			elif statusunit.status == '02':
				stat = 'Despachada'
			elif statusunit.status == '03':
				stat = 'Entregada'
			etree.SubElement(statuses,'status').text = date + ' ' + stat
		return etree.tostring(factura, pretty_print=True)

#Comercio genera una solicitud en el sistema

#Enviar factura a comercio
#Enviar factura a banco
#Problema con el id repetido en el xml factura
#@transaction.atomic
@csrf_exempt
def wsnewrequest(request):
	if request.method == 'POST':
		conttype = request.META['CONTENT_TYPE']
		if conttype == 'application/xml':
			xmlrequest = request.body
			dtdstring = StringIO.StringIO('<!ELEMENT despacho (id,comercio,productos,datosEnvio)><!ELEMENT id (#PCDATA)><!ELEMENT comercio (rif,nombre)><!ELEMENT rif (#PCDATA)><!ELEMENT nombre (#PCDATA)><!ELEMENT productos (producto+)><!ELEMENT producto (id,nombre,cantidad,medidas)><!ELEMENT id (#PCDATA)><!ELEMENT nombre (#PCDATA)><!ELEMENT cantidad (#PCDATA)><!ELEMENT medidas (peso,largo,ancho,alto)><!ELEMENT peso (#PCDATA)><!ELEMENT largo (#PCDATA)><!ELEMENT ancho (#PCDATA)><!ELEMENT alto (#PCDATA)><!ELEMENT datosEnvio (nombreDestinatario,telefonos,direccion,zip,ciudad,pais)><!ELEMENT nombreDestinatario (#PCDATA)><!ELEMENT telefonos (telefonoContacto+)><!ELEMENT telefonoContacto (#PCDATA)><!ELEMENT direccion (#PCDATA)><!ELEMENT zip (#PCDATA)><!ELEMENT ciudad (#PCDATA)><!ELEMENT pais (#PCDATA)>')
			dtd = etree.DTD(dtdstring)
			root = etree.XML(xmlrequest)
			if dtd.validate(root):
				associated = root[1]
				#print associated[0].text + ' ' + associated[1].text
				assoc_found = Associated.objects.filter(rif=associated[0].text,assoc_name=associated[1].text)
				if assoc_found.count() == 1:
					associated_comm = assoc_found.first()
					delcity = root[3][4].text
					delcountry = root[3][5].text
					delzip = root[3][3].text
					#Ruta destino
					locfound = Location.objects.filter(city=delcity,country=delcountry,zip_code=delzip)
					if locfound.count():
						location = locfound.first()
					else:
						location = Location(city=delcity,state=delcity,country=delcountry,zip_code=delzip)
						location.save()
					routefound = Route.objects.filter(destination=location)
					if routefound.count():
						route = routefound.first()
					else:
						route = Route(destination=location,charge_x_km=random.randrange(10,100,5))
						route.save()

					#Solicitud de envio
					dllist = DeliveryRequest.objects.order_by('id')
					lastdl = dllist[dllist.count()-1]
					number = 10000 + lastdl.id + 1
					tracking_number = (delcountry[0] + delcountry[1]).upper() + delzip.upper() + str(number)
					#print tracking_number

					daystodel = random.randrange(1,5,1)
					delivery_date = (datetime.utcnow()+timedelta(days=daystodel)).replace(tzinfo=utc)
					#print daystodel
					#print delivery_date

					address = root[3][2].text

					additional_info = 'Destinatario: ' + root[3][0].text + '\n'
					for telephone in root[3][1]:
						additional_info = additional_info + 'Teléfono: ' + telephone.text + '\n'
					#print additional_info

					newdelrequest = DeliveryRequest(
					tracking_number=tracking_number,
					delivery_date=delivery_date,
					address=address,
					additional_info=additional_info,
					route=route,
					associated_comm=associated_comm)	
					newdelrequest.save()

					locationfound = Location.objects.filter(
						city='Distribución',
						state='Distribución',
						country='Distribución',
						zip_code='Distribución')
					if locationfound.count():
						location = locationfound.first()
					else:
						location = Location(city='Distribución',state='Distribución',country='Distribución',zip_code='Distribución')
						location.save()

					#Estado de solicitud de envio
					newstatus = Status(
					status='00',
					location=location,
					delrequest=newdelrequest)
					newstatus.save()

					sub_total = 0
					#Paquetes vinculados a la solicitud
					for product in root[2]:
						description = product[1].text
						amount =int(product[2].text)
						weigth = product[3][0].text
						length = product[3][1].text
						width = product[3][2].text
						height = product[3][3].text
						price = (((float(length)*float(width)*float(height))/166)*route.charge_x_km)
						newpackage = Package(
							amount=amount,
							weigth=weigth,
							length=length,
							width=width,
							height=height,
							description=description,
							delivery_req=newdelrequest,
							price=price)
						#print description
						newpackage.save()
						sub_total = sub_total + amount*price

					#Factura vinculada a la solicitud
					dist = Distributor.objects.all().first()
					dist_rif = dist.rif
					dist_name = dist.dist_name
					taxes = sub_total*0.12
					total = sub_total + taxes
					banklist = Account.objects.all()
					totalacc = banklist.count()
					selectb = int(random.randrange(0,totalacc-1,1))
					#print selectb
					bank = banklist[selectb]
					account_number = bank.account_number

					newbill = Bill(
						dist_rif=dist_rif,
						dist_name=dist_name,
						account_number=account_number,
						sub_total=sub_total,
						taxes=taxes,
						total=total,
						payment_status='00',
						request=newdelrequest)
					newbill.save()
					
					#Registrar evento
					mssg = u'El comercio ' + associated_comm.assoc_name + u' ha generado una solicitud de envío en el sistema.'
					newlogentry = LogEntry(
						event_type='REQ',
						event_desc=mssg)
					newlogentry.save()

					#Construir respuesta
					print delivery_date
					#delivery_date_local = delivery_date.replace(tzinfo=get_current_timezone())
					delivery_date_local = delivery_date.astimezone(timezone('America/Caracas')).strftime('%d-%m-%Y %H:%M')
					print daystodel
					print delivery_date_local

					if newstatus.status == '00':
						stat = 'Recibido'
					elif newstatus.status == '01':
						stat = 'Por despachar'
					elif newstatus.status == '02':
						stat = 'Despachada'
					elif newstatus.status == '03':
						stat = 'Entregada'

					answer = etree.SubElement(root, 'respuesta')
					etree.SubElement(answer,'costo').text = str(total)
					etree.SubElement(answer,'fechaEntrega').text = str(delivery_date_local)
					etree.SubElement(answer,'tracking').text = str(tracking_number)
					etree.SubElement(answer,'estado').text = str(stat)
					#print etree.tostring(root, pretty_print=True)

					dtdstring = StringIO.StringIO('<!ELEMENT despacho (id,comercio,productos,datosEnvio,respuesta)><!ELEMENT id (#PCDATA)><!ELEMENT comercio (rif,nombre)><!ELEMENT rif (#PCDATA)><!ELEMENT nombre (#PCDATA)><!ELEMENT productos (producto+)><!ELEMENT producto (id,nombre,cantidad,medidas)><!ELEMENT id (#PCDATA)><!ELEMENT nombre (#PCDATA)><!ELEMENT cantidad (#PCDATA)><!ELEMENT medidas (peso,largo,ancho,alto)><!ELEMENT peso (#PCDATA)><!ELEMENT largo (#PCDATA)><!ELEMENT ancho (#PCDATA)><!ELEMENT alto (#PCDATA)><!ELEMENT datosEnvio (nombreDestinatario,telefonos,direccion,zip,ciudad,pais)><!ELEMENT nombreDestinatario (#PCDATA)><!ELEMENT telefonos (telefonoContacto+)><!ELEMENT telefonoContacto (#PCDATA)><!ELEMENT direccion (#PCDATA)><!ELEMENT zip (#PCDATA)><!ELEMENT ciudad (#PCDATA)><!ELEMENT pais (#PCDATA)><!ELEMENT respuesta (costo,fechaEntrega,tracking,estado)><!ELEMENT costo (#PCDATA)><!ELEMENT fechaEntrega (#PCDATA)><!ELEMENT tracking (#PCDATA)><!ELEMENT estado (#PCDATA)>')
					dtd = etree.DTD(dtdstring)
					#print dtd.validate(root)

					#Enviar factura a comercio
					reqbody = xmlbill(newbill.pk) 
					urlassc = associated_comm.bill_webservice
					#print urlassc
					ra = requests.post(urlassc,data=reqbody,headers={'content-type':'application/xml'})
					
					#Enviar factura a banco
					urlbank = bank.bill_webservice
					#print urlbank
					rb = requests.post(urlbank,data=reqbody,headers={'content-type':'application/xml'})
					

					return HttpResponse(etree.tostring(root, pretty_print=True),content_type='application/xml')
				else:
					print 'El comercio no se encuentra registrado'
					return HttpResponse(status=400)
			else:
				print 'No pase la validacion contra DTD'
				return HttpResponse(status=400)
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

def wsdetailrequest(request,requestid):
	delrequestlist = DeliveryRequest.objects.filter(tracking_number=requestid)
	if delrequestlist.count():
		delrequest = delrequestlist.first()
		requestbill = delrequest.bill  #try catch excepcion
		requeststatuslist = delrequest.status_set
		if requeststatuslist.count():
			requeststatus = requeststatuslist.first()
			if requeststatus.status == '00':
				stat = 'Recibido'
			elif requeststatus.status == '01':
				stat = 'Por despachar'
			elif requeststatus.status == '02':
				stat = 'Despachada'
			elif requeststatus.status == '03':
				stat = 'Entregada'
			
			#root = etree.XML('\\<?xml version="1.0"?>')
			#main = etree.ElementTree(root)
			dispatch = etree.Element('despacho')
			answer = etree.SubElement(dispatch, 'respuesta')
			etree.SubElement(answer,'costo').text = str(requestbill.total)
			etree.SubElement(answer,'fechaEntrega').text = str(
			(delrequest.delivery_date.astimezone(timezone('America/Caracas'))).strftime('%d-%m-%Y %H:%M'))
			etree.SubElement(answer,'tracking').text = str(delrequest.tracking_number)
			etree.SubElement(answer,'estado').text = str(stat)
			delrequestxml = etree.tostring(dispatch, pretty_print=True)
			
			return HttpResponse(delrequestxml,content_type='application/xml')
			#return HttpResponse(xmlbill(delrequest),content_type='application/xml')
		else:
			HttpResponse(status=400)
	else:
		return HttpResponse('No existe la solicitud.',content_type='text/plain')

def wsdetailbill(request,billid):
	reqbody = xmlbill(billid) 
	url = 'http://127.0.0.1:4567/comercio1/factura'
	r = requests.post(url,data=reqbody,headers={'content-type':'application/xml'})
	return HttpResponse(reqbody,content_type='application/xml') 
