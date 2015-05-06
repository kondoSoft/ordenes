#encoding:utf-8

from django.db import models
from django.contrib.auth.models import User


class clientes(models.Model):
	empresa = models.CharField(max_length=50, verbose_name=u'Empresa')
	nombre = models.CharField(max_length=50, verbose_name=u'Nombre(s)')
	apellido = models.CharField(max_length=50, verbose_name=u'Apellido(s)')
	direccion = models.CharField(max_length=250, verbose_name=u'Dirección')
	usuario = models.ForeignKey(User, verbose_name=u'Usuario')
	email = models.EmailField(verbose_name=u'Correo electrónico')
	fecha_alta = models.DateField(auto_now=True, verbose_name=u'Fecha Alta')
	estado_cliente = models.BooleanField(default=True, verbose_name=u'Estado')

	def __unicode__(self):
		return self.empresa

DURACION_SPOTS_CHOICES = (
	('seleccione', 'Seleccione duración'),
	('5', '5 SEG'),
	('10', '10 SEG'),
	('15', '15 SEG'),
	('20', '20 SEG'),
	('30', '30 SEG'),
	('60', '60 SEG'),
	('otro', 'Otra duracion'),
	)

class servicios(models.Model):
	nombre = models.CharField(max_length=70, verbose_name=u'Nombre del Spot')
	duracion = models.CharField(max_length=20, verbose_name=u'Duración del Spot', choices=DURACION_SPOTS_CHOICES, default='seleccione')
	otro = models.CharField(max_length=8, verbose_name=u'Otro', null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True, verbose_name=u'Script')
	archivo_texto = models.FileField(upload_to='archivo_texto', verbose_name=u'Archivo de texto', null=True, blank=True)
	archivo_referencia = models.FileField(upload_to='archivos_audio_video', verbose_name=u'Archivo de audio o video para referencia', null=True, blank=True)
	numero_orden = models.IntegerField(verbose_name=u'Servicios')
	fecha_orden = models.DateField(auto_now=True)
	usuario_enviar = models.ForeignKey(User, related_name='usuario_enviar', verbose_name=u'Destinatario')
	usuario = models.ForeignKey(User)
	

	def __unicode__(self):
		return self.nombre

class historial(models.Model):
	servicio = models.ForeignKey(servicios)
	duracion = models.CharField(max_length=20, verbose_name=u'Duración del Spot', choices=DURACION_SPOTS_CHOICES)
	otro = models.CharField(max_length=8, verbose_name=u'Otro', null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True, verbose_name=u'Script')
	archivo_texto = models.FileField(upload_to='archivos/', verbose_name=u'Archivo de texto', null=True, blank=True)
	archivo_referencia = models.FileField(upload_to='archivos/', verbose_name=u'Archivo de referencia', null=True, blank=True)
	fecha_cambio = models.DateField()
	usuario_enviar = models.ForeignKey(User, verbose_name=u'Destinatario')

	def __unicode__(self):
		return self.servicio

#nuevo