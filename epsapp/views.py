from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def testassets(request):
    #return HttpResponse('Hola')
    return render(request,'index.html')