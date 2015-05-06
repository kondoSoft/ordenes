from django.contrib.auth.forms import AdminPasswordChangeForm
from django.conf.urls import patterns, include, url
from django.conf import settings
from ordencliente import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from ordencliente.views import *
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'orden.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^$', views.lista_spots, name='inicio'),

                       # url(r'^perfil/chpasswd/done/?', 'django.contrib.auth.views.password_change_done'),

                       #url(r'^perfil/chpasswd/?', 'django.contrib.auth.views.password_change', name = 'profile-chpasswd'),

                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

                       url(r'^ordenes/$', 'ordencliente.views.ordenes', name='ordenes'),

                       url(r'^ordenes/editar/(?P<id_servicio>\d+)$', views.editar_orden, name='editar_orden'),

                       url(r'^usuarios_clientes/$', views.lista_usuarios, name='usuarios'),

                       url(r'^usuarios_admin/$', views.lista_usuarios_admin, name='usuarios_admin'),

                       url(r'^usuarios/editar/(?P<id_cliente>\d+)$', views.editar_usuario, name='editar_usuarios'),


                       url(r'^nuevo/$', views.nuevo_usuario, name='nuevo_usuario'),

                       url(r'^usuario/(?P<id_usuario>\d+)$', views.filtro_usuario, name='filtro_usuarios'),

                       url(r'^buscar/$', views.busqueda, name='busqueda'),

                       url(r'^reporte_general_pdf/$', views.reporte_general_pdf, name='reporte_general_pdf'),

                       url(r'^detalle/(?P<id_servicio>\d+)$', views.detalle_spot, name='detalle_spot'),

                       url(r'^lista_spots/(?P<id_usuario>\d+)$', views.lista_spots_usuarios,
                           name='lista_spots_usuarios'),

                       url(r'^lista_spots_pdf/(?P<id_usuario>\d+)$', views.lista_spots_usuarios_pdf,
                           name='lista_spots_usuarios_pdf'),

                       url(r'^detalle_spots_pdf/(?P<id_servicio>\d+)$', views.detalle_spots_usuarios_pdf,
                           name='detalle_spots_usuarios_pdf'),

                       url(r'^password/change/$',
                           auth_views.password_change,
                           name='password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='password_reset'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='password_reset_complete'),
                       #url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           #auth_views.password_reset_confirm,
                           #name='password_reset_confirm'),
                      url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),
                      url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),

                       #url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name="password_reset"),
                       #url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),

                       #url(r'^media/archivos/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}, name='archivos'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT, }),
)