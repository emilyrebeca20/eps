from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect
from epsapp.models import *
from django.contrib import messages
from django.shortcuts import render



def manager_required(view_func): 
	def _wrapped_view_func(request, *args, **kwargs):
		requser = request.user 
		#print requser.id
		userobjs = User.objects.filter(id=requser.id)
		if userobjs.count() == 1:
			userobj = userobjs.first()
			#print userobj
			profile = Employee.objects.filter(user=userobj)
			if profile.count() == 1:
				userprof = profile.first()
				if requser.is_authenticated() and userprof.role.role_name == 'Gerente':
					return view_func(request,*args, **kwargs)
		messages.error(request,'No tiene permisos para acceder.',extra_tags='danger')
		referer = request.META.get('HTTP_REFERER')
		if referer:
			return HttpResponseRedirect(referer)
		else:
			return render(request,'errtemplate.html')
	return _wrapped_view_func

def employee_required(view_func): 
	def _wrapped_view_func(request, *args, **kwargs):
		requser = request.user 
		userobjs = User.objects.filter(id=requser.id)
		if userobjs.count() == 1:
			userobj = userobjs.first()
			#print userobj
			profile = Employee.objects.filter(user=userobj)
			if profile.count() == 1:
				userprof = profile.first()
				if requser.is_authenticated() and (userprof.role.role_name == 'Gerente' or userprof.role.role_name == 'Despachador'):
					return view_func(request,*args, **kwargs)
		messages.error(request,'No tiene permisos para acceder.',extra_tags='danger')
		referer = request.META.get('HTTP_REFERER')
		if referer:
			return HttpResponseRedirect(referer)
		else:
			return render(request,'errtemplate.html')
	return _wrapped_view_func