from django.db import models
from datetime import timedelta, date, datetime
from django.utils.timezone import *
from django.contrib.auth.models import User

# Create your models here.

#Modelo Comercio
class Associated(models.Model): 
	"""docstring for Associated"""

	added = models.DateTimeField(verbose_name=u'Asociado en')
	rif = models.CharField(unique=True,max_length=50,verbose_name=u'RIF')
	assoc_name = models.CharField(max_length=100,verbose_name=u'Comercio')
	bill_webservice = models.URLField(verbose_name=u'URL del webservice')

	class Meta:
		verbose_name = 'Associated'
		verbose_name_plural = 'Associated'

	def __unicode__(self):
		return u'%s - Anadido: %s - RIF: %s' % (
			self.assoc_name,
			self.added,self.rif)

	def natural_key(self):
		return (self.added,self.rif,self.assoc_name)

#Modelo Ubicacion
class Location(models.Model):
	"""docstring for Location"""

	city = models.CharField(max_length=100,verbose_name=u'Ciudad')
	state = models.CharField(max_length=100,verbose_name=u'Estado')
	country = models.CharField(max_length=100,verbose_name=u'Pais')
	zip_code = models.CharField(unique=True,max_length=50,verbose_name=u'ZIP')

	class Meta:
		verbose_name = 'Location'
		verbose_name_plural = 'Locations'

	def __unicode__(self):
		return u'Ciudad: %s Estado: %s - ZIP: %s - Pais: %s' % (
			self.city,
			self.state,
			self.zip_code,
			self.country)
	
#Modelo Ruta
class Route(models.Model):
	"""docstring for Route"""
	
	destination = models.ForeignKey(Location,verbose_name=u'Destino')
	charge_x_km = models.FloatField(verbose_name=u'Costo por KM')

	class Meta:
		verbose_name = 'Route'
		verbose_name_plural = 'Routes'

	def __unicode__(self):
		return u'Ruta a %s con costo por KM de %s' % (
			self.destination,
			self.charge_x_km)

#Modelo Solicitud de envio
class DeliveryRequest(models.Model):
	"""docstring for DeliveryRequest"""
	
	request_date = models.DateTimeField(auto_now_add=True,verbose_name=u'Fecha de solicitud')
	tracking_number = models.CharField(unique=True,max_length=100,verbose_name=u'Numero de rastreo')
	delivery_date = models.DateTimeField(verbose_name=u'Fecha de entrega')
	address = models.TextField(verbose_name=u'Direccion')
	additional_info = models.TextField(blank=True,verbose_name=u'Informacion adicional')
	route = models.ForeignKey(Route,verbose_name=u'Ruta')
	associated_comm = models.ForeignKey(Associated,verbose_name=u'Comercio')

	class Meta:
		verbose_name = 'DeliveryRequest'
		verbose_name_plural = 'DeliveryRequests'

	def __unicode__(self):
		return u'%s Solicitada: %s - Tracking: %s - A: %s %s' % (
			self.id,
			self.request_date,
			self.tracking_number,
			self.route.destination,
			self.address)

#Modelo Estado
class Status(models.Model):
	"""docstring for Status"""
	DELIVERYREQUEST_STATUS = (
		('00','Recibida'),
		('01','Por despachar'),
		('02','Despachada'),
		('03','Entregada'))
	status = models.CharField(choices=DELIVERYREQUEST_STATUS,max_length=50,default='00',verbose_name=u'Estado')
	status_date = models.DateTimeField(auto_now=True,verbose_name=u'Fecha estado')
	location = models.ForeignKey(Location,verbose_name=u'Ubicacion')
	delrequest = models.ForeignKey(DeliveryRequest,verbose_name=u'Solicitud')

	class Meta:
		verbose_name = 'Status'
		verbose_name_plural = 'Status'
		ordering = ['status_date']

	def __unicode__(self):
		return u'%s %s %s' % (
			self.status,
			self.status_date,
			self.location)

#Modelo Paquete
class Package(models.Model):
	"""docstring for Package"""

	added_date = models.DateTimeField(auto_now_add=True,verbose_name=u'Agregado')
	amount = models.IntegerField(verbose_name=u'Cantidad')
	weigth = models.FloatField(verbose_name=u'Peso')
	length = models.FloatField(verbose_name=u'Largo')
	width = models.FloatField(verbose_name=u'Ancho')
	height = models.FloatField(verbose_name=u'Alto')
	description = models.TextField(blank=True,verbose_name=u'Descripcion')
	delivery_req = models.ForeignKey(DeliveryRequest,verbose_name=u'Solicitud')
	price = models.FloatField(verbose_name=u'Precio')

	class Meta:
		verbose_name = 'Package'
		verbose_name_plural = 'Packages'

	def __unicode__(self):
		return u'Cant %s - Agregado: %s - Peso: %s - Largo: %s - Ancho: %s - Alto: %s - Solicitud: %s' % (
			self.amount,
			self.added_date,
			self.weigth,
			self.length,
			self.width,
			self.height,
			self.delivery_req)

#Modelo Factura
class Bill(models.Model):
	"""docstring for Bill"""

	issuance_date = models.DateTimeField(auto_now_add=True,verbose_name=u'Generada')
	dist_rif = models.CharField(max_length=50,default='123456789',editable=False,verbose_name=u'RIF')
	dist_name = models.CharField(max_length=100,default='EPS Express',editable=False,verbose_name=u'Nombre distribuidor')
	account_number = models.CharField(max_length=100,default='0000000000000',editable=False,verbose_name=u'Numero de cuenta')
	sub_total = models.FloatField(default=0.0,editable=False,verbose_name=u'Sub-total')
	taxes = models.FloatField(default=0.0,editable=False,verbose_name=u'Impuestos')
	total = models.FloatField(default=0.0,editable=False,verbose_name=u'Total a pagar')
	expiration_date = models.DateTimeField(editable=False,verbose_name=u'Fecha de vencimiento')
	payment_date = models.DateTimeField(null=True,blank=True,verbose_name=u'Fecha de pago')
	PAYMENT_STATUS = (
		('00','Vigente'),
		('01','Cancelada'),
		('02','Vencida'),
		('03','Cancelada despues de fecha'))
	payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS,default='00',verbose_name=u'Estado del pago')
	request = models.OneToOneField(DeliveryRequest,verbose_name=u'Solicitud')

	class Meta:
		verbose_name = 'Bill'
		verbose_name_plural = 'Bills'

	def __unicode__(self):
		return u'%s - Comercio: %s - Generada: %s - Sub-total %s + Impuestos %s = Total %s - %s - Pagada el: %s - Se vence: %s - Pagar en: %s' % (
			self.request.tracking_number,
			self.request.associated_comm,
			self.issuance_date,
			self.sub_total,
			self.taxes,self.total,
			self.payment_status,
			self.payment_date,
			self.expiration_date,
			self.account_number)

	def save(self,*args,**kwargs):
		if not self.id:
			self.expiration_date = (datetime.utcnow()+timedelta(days=30)).replace(tzinfo=utc)
		super(Bill,self).save(args,kwargs)

#Modelo Tipo de empleado
class Role(models.Model):
	"""docstring for Role"""
	
	role_name = models.CharField(max_length=50,verbose_name=u'Tipo de empleado')

	class Meta:
		verbose_name = 'Role'
		verbose_name_plural = 'Roles'

	def __unicode__(self):
		return u'Rol: %s' % (self.role_name)

#Modelo Empleado
class Employee(models.Model):
	"""docstring for Employee"""

	user = models.OneToOneField(User,verbose_name=u'Usuario')
	hire_date = models.DateField(auto_now_add=True,editable=False,verbose_name=u'Fecha contratacion')
	ci = models.CharField(unique=True,max_length=50,verbose_name=u'Cedula')
	middle_name = models.CharField(max_length=50,blank=True,verbose_name=u'Segundo Nombre')
	second_last_name = models.CharField(max_length=50,blank=True,verbose_name=u'Segundo Apellido')
	phone = models.CharField(max_length=50,verbose_name=u'Telefono')
	cellphone = models.CharField(max_length=50,verbose_name=u'Celular')
	address = models.TextField(verbose_name=u'Direccion')
	role = models.ForeignKey(Role,verbose_name=u'Tipo de empleado')

	class Meta:
		verbose_name = 'Employee'
		verbose_name_plural = 'Employees'

	def __unicode__(self):
		return u'%s %s %s %s %s %s' % (self.user,self.user.first_name,self.user.last_name,self.ci,self.phone,self.role)
				
#Modelo entrada del registro
class LogEntry(models.Model):
	"""docstring for LogEntry"""

	event_date = models.DateTimeField(auto_now_add=True,verbose_name=u'Marca de tiempo')
	LOGEVENT_TYPE = (('ERR','Error'),('REQ','Solicitud'),('EMP','Empleado'),('PAY','Pago'),('GEN','General')) 
	event_type = models.CharField(choices=LOGEVENT_TYPE,max_length=50,verbose_name=u'Tipo de evento')
	event_desc = models.TextField(verbose_name=u'Descripcion')

	class Meta:
		verbose_name = 'LogEntry'
		verbose_name_plural = 'LogEntrys'

	def __unicode__(self):
		dis_datetime = self.event_date
		return u'%s %s %s' % (
			self.event_date.astimezone(tz=get_default_timezone()), 
			self.event_type,
			self.event_desc)

#Modelo Reporte
class Report(models.Model):
	"""docstring for Report"""

	date_created = models.DateTimeField(auto_now_add=True,verbose_name=u'Fecha de creacion')
	int_init = models.DateTimeField(verbose_name=u'Inicio intervalo')
	int_end = models.DateTimeField(verbose_name=u'Fin intervalo')
	REPORT_TYPES = (
		('01','Solicitudes despachadas y tiempo de despacho'),
		('02','Solicitudes pendientes y tiempo pendiente'),
		('03','Clientes ordenados por cantidad de solicitudes'),
		('04','Destinos ordenados por cantidad de solicitudes'),
		('05','Facturas ordenadas por tiempo de cancelacion'),
		('06','Facturas vigentes por cobrar'),
		('07','Facturas vencidas por cobrar'),
		)
	type = models.CharField(max_length=50,verbose_name=u'Tipo de reporte')
	pdf_path = models.FilePathField(null=True,blank=True,path="static/pdf/reports",match=".*\.pdf",verbose_name=u'Archivo PDF')
	employee = models.ForeignKey(Employee,verbose_name=u'Empleado')

	class Meta:
		verbose_name = 'Report'
		verbose_name_plural = 'Reports'

	def __unicode__(self):
		return u'Creado por: %s en %s Intervalo: %s - %s %s' % (
			self.employee,
			self.date_created,
			self.int_init,
			self.int_end,
			self.type)

#Modelo cuenta de				
class Account(models.Model): 
	"""docstring for BankAccount"""

	bank_name = models.CharField(max_length=100,verbose_name=u'Banco')
	account_number = models.CharField(max_length=100,verbose_name=u'Numero de cuenta')
	bill_webservice = models.URLField(verbose_name=u'URL del webservice')

	class Meta:
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'

	def __unicode__(self):
		return u'%s %s en %s' % (
			self.bank_name,
			self.account_number,
			str(self.bill_webservice))

	# def __init__(self, arg):
	# 	super(Bank, self).__init__()
	# 	self.arg = arg
		

# class Manager(Employee):
# 	"""docstring for Manager"""

# 	class Meta:
# 		verbose_name = 'Manager'
# 		verbose_name_plural = 'Managers'

# 	def __unicode__(self):
# 		pass

# 	def __init__(self, arg):
# 		super(Manager, self).__init__()
# 		self.arg = arg
		
# class Distpatcher(Employee):
# 	"""docstring for Distpatcher"""

# 	class Meta:
# 		verbose_name = 'Distpatcher'
# 		verbose_name_plural = 'Distpatchers'

# 	def __unicode__(self):
# 		pass

# 	def __init__(self, arg):
# 		super(Manager, self).__init__()
# 		self.arg = arg

# 	def __init__(self, arg):
# 		super(Distpatcher, self).__init__()
# 		self.arg = arg