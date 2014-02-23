from django.shortcuts import render
from django.http import HttpResponse
from datetime import *
from epsapp.models import *

# Create your views here.

#Renderiza la plantilla padre
def home(request):
    #return HttpResponse('Hola')
    return render(request,'home.html')


def tracking(request):
	tn = request.GET['trackingn']
	DeliveryRequest.
	return HttpResponse(tn)