# encoding:utf-8
from django.conf import settings
import os

from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from ordencliente.models import *
from orden.forms import *
from datetime import date
from datetime import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
import smtplib
from django.core.mail import EmailMessage
# Create your views here.
ERROR_MESSAGE = 'Por favor, corrija el siguiente error'


@login_required
def principal(request):
    inicio = 'active'
    paquete = {'inicio': inicio, }
    return render_to_response('principal.html',
                              paquete, context_instance=RequestContext(request))


@login_required
def ordenes(request):
    usuarios = User.objects.get(pk=request.user.id)
    correo = usuarios.email
    usuario = usuarios.username

    if request.method == 'POST':
        ordenform = ClienteForm(request.POST, request.FILES)
        if ordenform.is_valid():
            nombre = ordenform.cleaned_data['nombre']
            duracion = ordenform.cleaned_data['duracion']
            otro = ordenform.cleaned_data['otro']
            descripcion = ordenform.cleaned_data['descripcion']
            archivo_texto = ordenform.cleaned_data['archivo_texto']
            archivo_referencia = ordenform.cleaned_data['archivo_referencia']
            usuario_enviar = ordenform.cleaned_data['usuario_enviar']

            correo_destinatario = User.objects.get(username=usuario_enviar)
            enviar_correo = correo_destinatario.email

            x = servicios()
            x.nombre = nombre

            x.duracion = duracion
            x.otro = otro
            x.descripcion = descripcion
            x.archivo_texto = archivo_texto
            x.archivo_referencia = archivo_referencia
            x.usuario_enviar = usuario_enviar
            x.usuario = request.user
            x.numero_orden = 1

            subject = 'Notificación de spot nuevo'
            from_email = correo
            to = 'pacocorrea@grupoquatro.com'
            #to = 'juarezm_90@hotmail.com'
            cc = enviar_correo
            text_content = 'Mensaje importante.'
            html_content = 'El usuario ' + '<b>' + usuario + '</b>' + ' con correo ' + '<b>' + correo + '</b>' ' ha creado el spot ' + '<b>' + nombre + '</b>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [cc])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            x.save()

            messages.success(request, 'Spot registrado satisfactoriamente')

            return HttpResponseRedirect('/')
        else:
            messages.error(request, ERROR_MESSAGE)
    else:
        ordenform = ClienteForm()
    return render_to_response('registrar_spot.html', {'ordenform': ordenform}, context_instance=RequestContext(request))


@login_required
def editar_orden(request, id_servicio):
    servicio = servicios.objects.get(pk=id_servicio)
    usuarios = User.objects.get(pk=request.user.id)
    correo = usuarios.email
    usuario = usuarios.username
    if request.method == 'GET':
        ordenform = ClienteForm(initial={'nombre': servicio.nombre,
                                         'duracion': servicio.duracion,
                                         'descripcion': servicio.descripcion,
                                         'archivo_texto': servicio.archivo_texto,
                                         'archivo_referencia': servicio.archivo_referencia

                                         })
    elif request.method == 'POST':
        ordenform = ClienteForm(request.POST, request.FILES)
        if ordenform.is_valid():
            fecha_cambio = date.today()
            duracion = ordenform.cleaned_data['duracion']
            otro = ordenform.cleaned_data['otro']
            descripcion = ordenform.cleaned_data['descripcion']
            archivo_texto = ordenform.cleaned_data['archivo_texto']
            archivo_referencia = ordenform.cleaned_data['archivo_referencia']
            usuario_enviar = ordenform.cleaned_data['usuario_enviar']

            correo_destinatario = User.objects.get(username=usuario_enviar)
            enviar_correo = correo_destinatario.email

            servicio.numero_orden = servicio.numero_orden + 1

            historia = historial()
            historia.fecha_cambio = fecha_cambio
            historia.duracion = duracion
            historia.otro = otro
            historia.descripcion = descripcion
            historia.archivo_texto = archivo_texto
            historia.archivo_referencia = archivo_referencia
            historia.usuario_enviar = usuario_enviar
            historia.servicio = servicio

            subject = 'Notificación de spot editado'
            from_email = correo
            to = 'pacocorrea@grupoquatro.com'
            cc = enviar_correo
            text_content = 'Mensaje importante.'
            html_content = 'El usuario ' + '<b>' + usuario + '</b>' + ' con correo ' + '<b>' + correo + '</b>' ' ha editado el spot ' + '<b>' + servicio.nombre + '</b>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [cc])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            servicio.save()
            historia.save()

            messages.success(request, 'Spot editado satisfactoriamente')

            return HttpResponseRedirect('/')
        else:
            messages.error(request, ERROR_MESSAGE)
    else:
        ordenform = ClienteForm()
    return render_to_response('registrar_spot.html', {'servicio': servicio, 'ordenform': ordenform, 'variable': '1'},
                              context_instance=RequestContext(request))


@login_required
def nuevo_usuario(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            empresa = form.cleaned_data['empresa']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            usuario = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            staff = form.cleaned_data['staff']
            if staff:
                staff = True
                u = User.objects.create_user(username=usuario, email=email, password=password_one)
                u.is_staff = staff
            else:
                staff = False
                u = User.objects.create_user(username=usuario, email=email, password=password_one)

            u.save()
            cliente = clientes()
            cliente.empresa = empresa
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.direccion = direccion
            cliente.usuario = u
            cliente.email = u.email
            cliente.save()
            messages.success(request, 'Usuario creado satisfactoriamente')
            return HttpResponseRedirect('/nuevo/')
        else:
            messages.error(request, ERROR_MESSAGE)
    else:
        form = RegisterForm()
    return render_to_response('registrar.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def editar_usuario(request, id_cliente):
    cuenta = clientes.objects.get(pk=id_cliente)
    usuario = User.objects.get(pk=cuenta.usuario.id)
    if request.method == 'POST':
        form = NuevoClienteForm(request.POST, instance=cuenta)
        if form.is_valid():
            empresa = form.cleaned_data['empresa']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            email = form.cleaned_data['email']
            #estado_cliente = form.cleaned_data['estado_cliente']

            cuenta.empresa = empresa
            cuenta.nombre = nombre
            cuenta.apellido = apellido
            cuenta.direccion = direccion
            cuenta.email = email
            #cuenta.estado_cliente = estado_cliente
            cuenta.save()

            usuario.email = email
            #usuario.is_active = estado_cliente
            usuario.save()

            messages.success(request, 'Usuario editado satisfactoriamente')
            return HttpResponseRedirect('/usuarios_clientes/')
        else:
            messages.error(request, ERROR_MESSAGE)
    else:
        form = NuevoClienteForm(instance=cuenta)
    return render_to_response('registrar.html', {'cuenta': cuenta, 'form': form},
                              context_instance=RequestContext(request))

@login_required
def editar_usuario_admin(request, id_cliente):
    cuenta = clientes.objects.get(pk=id_cliente)
    usuario = User.objects.get(pk=cuenta.usuario.id)
    if request.method == 'POST':
        form = NuevoClienteForm(request.POST, instance=cuenta)
        if form.is_valid():
            empresa = form.cleaned_data['empresa']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            email = form.cleaned_data['email']
            #estado_cliente = form.cleaned_data['estado_cliente']

            cuenta.empresa = empresa
            cuenta.nombre = nombre
            cuenta.apellido = apellido
            cuenta.direccion = direccion
            cuenta.email = email
            #cuenta.estado_cliente = estado_cliente
            cuenta.save()

            usuario.email = email
            #usuario.is_active = estado_cliente
            usuario.save()

            messages.success(request, 'Usuario editado satisfactoriamente')
            return HttpResponseRedirect('/usuarios_admin/')
        else:
            messages.error(request, ERROR_MESSAGE)
    else:
        form = NuevoClienteForm(instance=cuenta)
    return render_to_response('registrar.html', {'cuenta': cuenta, 'form': form},
                              context_instance=RequestContext(request))


@login_required
def lista_usuarios(request):
    cliente = clientes.objects.filter(usuario__is_staff=False).order_by('nombre')
    paginator = Paginator(cliente, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        cliente = paginator.page(page)
    except (InvalidPage, EmptyPage):
        cliente = paginator.page(paginator.num_pages)
    return render_to_response('usuarios.html', {'cliente': cliente, }, context_instance=RequestContext(request))


@login_required
def lista_usuarios_admin(request):
    admin_usuario = clientes.objects.filter(usuario__is_staff=True).order_by('nombre')

    paginar = Paginator(admin_usuario, 15)

    try:
        pagina = int(request.GET.get("page", '1'))
    except ValueError:
        pagina = 1

    try:
        admin_usuario = paginar.page(pagina)
    except (InvalidPage, EmptyPage):
        admin_usuario = paginar.page(paginar.num_pages)
    return render_to_response('usuarios_admin.html', {'admin_usuario': admin_usuario, },
                              context_instance=RequestContext(request))


@login_required
def lista_spots(request):
    fecha = date.today()
    mes = fecha.month
    usuarios = User.objects.filter(is_active=True, is_staff=False).order_by('username')
    paginator = Paginator(usuarios, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        usuarios = paginator.page(page)
    except (InvalidPage, EmptyPage):
        usuarios = paginator.page(paginator.num_pages)
    usuario_admin = servicios.objects.all().order_by('usuario')
    paginator = Paginator(usuario_admin, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        usuario_admin = paginator.page(page)
    except (InvalidPage, EmptyPage):
        usuario_admin = paginator.page(paginator.num_pages)
    x = request.user.id
    servicio = servicios.objects.filter(usuario=x)
    paginator = Paginator(servicio, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        servicio = paginator.page(page)
    except (InvalidPage, EmptyPage):
        servicio = paginator.page(paginator.num_pages)
    usuario_staff = servicios.objects.filter(usuario_enviar=request.user, fecha_orden__month=mes)
    cambios_spot_staff = historial.objects.filter(usuario_enviar=request.user, fecha_cambio__month=mes)
    return render_to_response('principal.html',
                              {'usuario_staff': usuario_staff, 'cambios_spot_staff': cambios_spot_staff,
                               'usuario_admin': usuario_admin, 'servicio': servicio, 'usuarios': usuarios},
                              context_instance=RequestContext(request))


@login_required
def lista_spots_admin(request):
    usuarios = User.objects.all().order_by('username')
    paginator = Paginator(usuarios, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        usuarios = paginator.page(page)
    except (InvalidPage, EmptyPage):
        usuarios = paginator.page(paginator.num_pages)
    return render_to_response('principal.html', {'usuarios': usuarios}, context_instance=RequestContext(request))


@login_required
def lista_spots_usuarios(request, id_usuario):
    fecha = date.today()
    mes = fecha.month
    spots = servicios.objects.filter(usuario=id_usuario, fecha_orden__month=mes)
    paginator = Paginator(spots, 15)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        spots = paginator.page(page)
    except (InvalidPage, EmptyPage):
        spots = paginator.page(paginator.num_pages)
    return render_to_response('lista_spots_usuario.html', {'spots': spots}, context_instance=RequestContext(request))


@login_required
def detalle_spot(request, id_servicio):
    dato = servicios.objects.get(pk=id_servicio)
    historia = historial.objects.filter(servicio=id_servicio)

    return render_to_response('detalles_spots.html', {'dato': dato, 'historia': historia},
                              context_instance=RequestContext(request))


@login_required
def filtro_usuario(request, id_usuario):
    usuarios = User.objects.all().order_by('username')
    usuario_admin = servicios.objects.filter(usuario=id_usuario)
    return render_to_response('principal.html',
                              {'usuario_admin': usuario_admin, 'usuarios': usuarios, 'id_usuario': id_usuario},
                              context_instance=RequestContext(request))


@login_required
def busqueda(request):
    buscar = request.POST.get('buscar')
    historia = ''
    consulta = ''
    fecha_1 = request.POST.get('f_inicial')
    fecha_2 = request.POST.get('f_final')
    if fecha_1 and fecha_2:
        fecha_ini = datetime.strptime(fecha_1, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_2, "%d/%m/%Y")
        consulta = servicios.objects.filter(fecha_orden__range=(fecha_ini, fecha_fin))
        historia = historial.objects.filter(fecha_cambio__range=(fecha_ini, fecha_fin))
    if buscar:
        consulta = servicios.objects.filter(usuario__username=buscar)
        for h in consulta:
            historia = historial.objects.filter(servicio__usuario=h.usuario)
    return render_to_response('busqueda.html',
                              {'consulta': consulta, 'fecha_1': fecha_1, 'fecha_2': fecha_2, 'buscar': buscar,
                               'historia': historia}, context_instance=RequestContext(request))


def usuario_admin_activar(request, id_usuario):
    usuario_ = clientes.objects.get(pk=id_usuario)
    usuario_ad_ = User.objects.get(pk=usuario_.usuario.pk)
    usuario_.estado_cliente = True
    usuario_ad_.is_active = True
    usuario_.save()
    usuario_ad_.save()
    return HttpResponseRedirect('/usuarios_admin/')

def usuario_admin_desactivar(request, id_usuario):
    usuario_ = clientes.objects.get(pk=id_usuario)
    usuario_ad_ = User.objects.get(pk=usuario_.usuario.pk)
    usuario_.estado_cliente = False
    usuario_ad_.is_active = False
    usuario_.save()
    usuario_ad_.save()
    return HttpResponseRedirect('/usuarios_admin/')

def usuario_activar(request, id_usuario):
    usuario_ = clientes.objects.get(pk=id_usuario)
    usuario_ad_ = User.objects.get(pk=usuario_.usuario.pk)
    usuario_.estado_cliente = True
    usuario_ad_.is_active = True
    usuario_.save()
    usuario_ad_.save()
    return HttpResponseRedirect('/usuarios_clientes/')

def usuario_desactivar(request, id_usuario):
    usuario_ = clientes.objects.get(pk=id_usuario)
    usuario_ad_ = User.objects.get(pk=usuario_.usuario.pk)
    usuario_.estado_cliente = False
    usuario_ad_.is_active = False
    usuario_.save()
    usuario_ad_.save()
    return HttpResponseRedirect('/usuarios_clientes/')


#===============================================================================================================
#para crear pdf
#===============================================================================================================


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     context = Context(context_dict)
#     html  = template.render(context)
#     result = StringIO.StringIO()
#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
#     if not pdf.err:
#         return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
#     return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def render_to_pdf(template_src, context_dict):
    """Function to render html template into a pdf file"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                            dest=result,
                            encoding='UTF-8',
                            link_callback=fetch_resources)
    if not pdf.err:
        response = http.HttpResponse(result.getvalue(), content_type='application/pdf')
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def fetch_resources(uri, rel):
    import os.path
    from django.conf import settings

    path = os.path.join(
        settings.STATIC_ROOT,
        uri.replace(settings.STATIC_URL, "/static/"))
    return path


@login_required
def lista_spots_usuarios_pdf(request, id_usuario):
    spots = servicios.objects.filter(usuario=id_usuario)
    return render_to_pdf('lista_spots_usuario_pdf.html', {'pagesize': 'A4', 'spots': spots, 'usuario': id_usuario})


@login_required
def detalle_spots_usuarios_pdf(request, id_servicio):
    dato = servicios.objects.get(pk=id_servicio)
    historia = historial.objects.filter(servicio=id_servicio).order_by('id')
    return render_to_pdf('detalle_spots_usuario_pdf.html', {'pagesize': 'letter', 'dato': dato, 'historia': historia})


@login_required
def reporte_general_pdf(request):
    buscar = request.POST.get('buscar')
    historia = ''
    consulta = ''
    fecha_1 = request.POST.get('f_inicial')
    fecha_2 = request.POST.get('f_final')
    if fecha_1 and fecha_2:
        fecha_ini = datetime.strptime(fecha_1, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_2, "%d/%m/%Y")
        consulta = servicios.objects.filter(fecha_orden__range=(fecha_ini, fecha_fin))
        historia = historial.objects.filter(fecha_cambio__range=(fecha_ini, fecha_fin))
    if buscar:
        consulta = servicios.objects.filter(usuario__username=buscar)
        #Q(nombre__icontains=buscar))
        for h in consulta:
            historia = historial.objects.filter(servicio__usuario=h.usuario)
    return render_to_pdf('reporte_general_pdf.html',
                         {'pagesize': 'A4', 'fecha_1': fecha_1, 'fecha_2': fecha_2, 'consulta': consulta,
                          'historia': historia})
