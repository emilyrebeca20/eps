from django.shortcuts import render
from django.http import *
from datetime import *
from epsapp.models import *
from django.core import serializers
from django.contrib import messages

# Create your views here.

#Renderiza la plantilla padre
def home(request):
    #return HttpResponse('Hola')
    return render(request,'home.html')


def tracking(request):
	params = request.GET 
	if 'trackingn' in params:
		trackingnum = params['trackingn']
		delivery_req = DeliveryRequest.objects.filter(tracking_number=trackingnum)
		if delivery_req.count() == 1:
			delivery_req_json = serializers.serialize("json", [delivery_req.first(),],use_natural_keys=True)
			return render(request,'trackinginfo.html',{"deliveryreq":delivery_req.first()})
		else:
			messages.error(request,'La solicitud requerida no existe.',extra_tags='danger')
			return render(request,'trackinginfo.html')
	else:
		return HttpResponse(status=400)
	