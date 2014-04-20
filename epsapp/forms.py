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

	status = forms.ChoiceField(choices=DELIVERYREQUEST_STATUS,label='Estado')
	location = LocationChoiceField(queryset=Location.objects.all(),empty_label=None,label='Locación')

