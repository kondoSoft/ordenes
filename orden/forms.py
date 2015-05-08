# encoding:utf-8
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from ordencliente.models import *
from django.contrib.auth.models import User
from django.forms.widgets import *
import datetime
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget


class ClienteForm(forms.ModelForm):
    usuario_enviar = forms.ModelChoiceField(empty_label='Seleccione destinatario',
                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=User.objects.filter(is_staff=True).exclude(is_superuser=True))

    class Meta:
        model = servicios
        fields = ('nombre', 'duracion', 'otro', 'descripcion', 'archivo_texto', 'archivo_referencia', 'usuario_enviar')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del spot'}),
            'duracion': Select(attrs={'class': 'form-control'}),
            'otro': TextInput(attrs={'class': ' form-control', 'placeholder': 'De ser otra duracion espefique aquí'}),
            'descripcion': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Script o descripción del contenido del spot'}),
            'archivo_texto': FileInput(attrs={'class': '', 'accept': '.pdf, .doc, .docx, .odt, .pptx, .ppt'}),
            'archivo_referencia': FileInput(
                attrs={'class': '', 'accept': '.mp3, .mp4, .avi, .mpg, .mov, .flv, .wma, .m4v, .3gp'}),
            'numero_orden': TextInput(attrs={'class': 'validate[required] form-control placeholder'}),
            'usuario': Select(attrs={'class': 'validate[required] form-control placeholder'}),

        }


class NuevoClienteForm(forms.ModelForm):
    #email = forms.EmailField(label='Correo Electronico', widget=forms.TextInput(attrs={'class':'validate[required] form-control placeholder'}))
    class Meta:
        model = clientes
        fields = ('empresa', 'nombre', 'apellido', 'direccion', 'email', 'estado_cliente')
        widgets = {
        'empresa': TextInput(attrs={'class': 'validate[required] form-control placeholder'}),
        'nombre': TextInput(attrs={'class': 'validate[required] form-control placeholder'}),
        'apellido': TextInput(attrs={'class': 'validate[required] form-control placeholder'}),
        'direccion': TextInput(attrs={'class': 'validate[required] form-control placeholder'}),
        'email': TextInput(attrs={'class': 'form-control'}),
        'usuario': Select(attrs={'class': 'validate[required] form-control placeholder'}),
        }

        exclude = ['estado_cliente']


class RegisterForm(forms.Form):
    empresa = forms.CharField(label='Nombre de la compañia',
                              widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    nombre = forms.CharField(label='Nombre(s)',
                             widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    apellido = forms.CharField(label='Apellido(s)',
                               widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    direccion = forms.CharField(label='Dirección',
                                widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    username = forms.CharField(label="Nombre de Usuario",
                               widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    email = forms.EmailField(label='Correo Electronico',
                             widget=forms.TextInput(attrs={'class': 'validate[required] form-control placeholder'}))
    password_one = forms.CharField(label='Contraseña', min_length=8, widget=forms.PasswordInput(render_value=False,
                                                                                                attrs={
                                                                                                'class': 'validate[required] form-control placeholder'}))
    password_two = forms.CharField(label='Confirmar contraseña', min_length=8,
                                   widget=forms.PasswordInput(render_value=False, attrs={
                                   'class': 'validate[required] form-control placeholder'}))
    staff = forms.BooleanField(required=False, label="Usuario staff")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('El nombre de usuario ya existe')

    def clean_password_two(self):
        password_one = self.cleaned_data.get('password_one', '')
        password_two = self.cleaned_data.get('password_two', '')
        if password_one != password_two:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password_two