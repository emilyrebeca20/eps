# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import *
from datetime import *
from epsapp.models import *
from epsapp.decorators import *
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import *
from django.template import RequestContext,Context


# Create your views here.

#Renderiza la plantilla padre
def home(request):
	return render(request,'home.html')


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

def empmain(request):
	return render(request,'empmain.html')

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

@manager_required
def manager(request):
	return render(request,'managermain.html')

@employee_required
def dispatcher(request):
	return render(request,'employeemain.html')

@employee_required
def alldelrequest_disp(request):
	delrequests = DeliveryRequest.objects.all()
	if delrequests.count() <= 0:
		messages.warning(request,'No existen solicitudes registradas en el sistema.',extra_tags='warning')
	return render(request,'deliveryrequest-disp.html',{'delrequests':delrequests})
	
@manager_required
def alldelrequest_man(request):
	delrequests = DeliveryRequest.objects.all()
	if delrequests.count() <= 0:
		messages.warning(request,'No existen solicitudes registradas en el sistema.',extra_tags='warning')
	return render(request,'deliveryrequest-man.html',{'delrequests':delrequests})

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

@employee_required
def deletereq(request,requestid):
	if request.method == 'GET':
		if requestid:
			delivery_req = DeliveryRequest.objects.filter(id=requestid)
			if delivery_req.count() == 1:
				delivery_req.first().delete()
				messages.success(request,'La solicitud ha sido eliminada.',extra_tags='success')
				return HttpResponseRedirect('/appeps/gerente/solicitudes')
			else:
				messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
				return render(request,'errtemplate.html')
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

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

@manager_required
def routes(request):
	return render(request,'routes-man.html')

@manager_required
def reports(request):
	return render(request,'reports-man.html')

@manager_required
def logs(request):
	logentrys = LogEntry.objects.all()
	return render(request,'logs-man.html',{'logentrys':logentrys})

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

def emplogout(request):
	logout(request)
	messages.success(request,'Cierre de sesión exitoso.',extra_tags='success')
	return HttpResponseRedirect('/appeps')

def exception(request):
	render(request,'errtemplate.html')

#Cruds

@employee_required
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
