from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Renderiza la plantilla padre
def home(request):
    #return HttpResponse('Hola')
    return render(request,'home.html')