# -*- coding: utf-8 -*-
from django import forms
from epsapp.models import *

class LocationChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return '%s, %s, %s, %s' % (obj.country,obj.state,obj.city,obj.zip_code)

class UpdateStatusForm(forms.Form):
	
	DELIVERYREQUEST_STATUS = (
	('00','Recibida'),
	('01','Por despachar'),
	('02','Despachada'),
	('03','Entregada'))

	status = forms.ChoiceField(choices=DELIVERYREQUEST_STATUS,label='Estado',required=True)
	location = LocationChoiceField(queryset=Location.objects.all(),empty_label=None,label='Locación',required=True)


class CreateReportForm(forms.Form):
	int_init = forms.DateTimeField(label='Inicio de intervalo')
	int_end = forms.DateTimeField(label='Fin de intervalo')
	REPORT_TYPES = (
		('01','Solicitudes despachadas y tiempo de despacho'),
		('02','Solicitudes pendientes y tiempo pendiente'),
		('03','Clientes ordenados por cantidad de solicitudes'),
		('04','Destinos ordenados por cantidad de solicitudes'),
		('05','Facturas ordenadas por tiempo de cancelacion'),
		('06','Facturas vigentes por cobrar'),
		('07','Facturas vencidas por cobrar'),
		)
	type = forms.ChoiceField(choices=REPORT_TYPES,label='Tipo de reporte',required=True)