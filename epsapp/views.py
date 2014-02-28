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
				#delivery_req_json = serializers.serialize("json", [delivery_req.first(),],use_natural_keys=True)
				return render(request,'trackinginfo.html',{"deliveryreq":delivery_req.first()})
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
	#print "Hola"
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
				# the authentication system was unable to verify the username and password
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
	return render(request,'deliveryrequest-disp.html')
	
@manager_required
def alldelrequest_man(request):
	return render(request,'deliveryrequest-man.html')

@manager_required
def reports(request):
	return render(request,'reports-man.html')

@manager_required
def logs(request):
	return render(request,'logs-man.html')

def emplogout(request):
	logout(request)
	messages.success(request,'Cierre de sesión exitoso.',extra_tags='success')
	return HttpResponseRedirect('/appeps')

def exception(request):
	render(request,'errtemplate.html')