# ============================================================
# FORMULARIOS - reservas/forms.py
# Los formularios en Django validan los datos que el usuario
# envía. Cada ModelForm se conecta a un modelo automáticamente.
# ============================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Complejo, Cancha, Reserva, TipoCancha


# -------------------------------------------------------
# FORMULARIO: Registro de Usuario
# Hereda de UserCreationForm que ya trae campos de contraseña
# con confirmación y validaciones.
# -------------------------------------------------------
class RegistroForm(UserCreationForm):
    # Campos adicionales que queremos en el formulario de registro
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu apellido'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+57 300 000 0000'
        })
    )

    class Meta:
        # Le decimos que use el modelo Usuario
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos los widgets de los campos de contraseña
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirmar contraseña'})
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"


# -------------------------------------------------------
# FORMULARIO: Login personalizado
# -------------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu contraseña'
        })
    )


# -------------------------------------------------------
# FORMULARIO: Complejo Deportivo
# ModelForm genera automáticamente los campos desde el modelo
# -------------------------------------------------------
class ComplejoForm(forms.ModelForm):
    class Meta:
        model = Complejo
        fields = ['nombre_com', 'ubicacion_com']
        labels = {
            'nombre_com': 'Nombre del Complejo',
            'ubicacion_com': 'Dirección / Ubicación',
        }
        widgets = {
            'nombre_com': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Complejo Deportivo Norte'
            }),
            'ubicacion_com': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Dirección completa del complejo'
            }),
        }


# -------------------------------------------------------
# FORMULARIO: Cancha
# -------------------------------------------------------
class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['id_complejo', 'nombre_cancha', 'id_tipo_can', 'capacidad_can', 'precio_hora', 'descripcion', 'activa']
        labels = {
            'id_complejo': 'Complejo',
            'nombre_cancha': 'Nombre de la Cancha',
            'id_tipo_can': 'Tipo de Cancha',
            'capacidad_can': 'Capacidad (personas)',
            'precio_hora': 'Precio por Hora ($)',
            'descripcion': 'Descripción',
            'activa': '¿Cancha activa?',
        }
        widgets = {
            'nombre_cancha': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Cancha A'}),
            'capacidad_can': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'precio_hora': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'id_complejo': forms.Select(attrs={'class': 'form-select'}),
            'id_tipo_can': forms.Select(attrs={'class': 'form-select'}),
        }


# -------------------------------------------------------
# FORMULARIO: Reserva
# -------------------------------------------------------
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['id_cancha', 'fecha', 'hora_inicio', 'hora_fin']
        labels = {
            'id_cancha': 'Cancha',
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
        }
        widgets = {
            'id_cancha': forms.Select(attrs={'class': 'form-select'}),
            # type="date" muestra un selector de fecha en el navegador
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
        }

    def clean(self):
        # Validaciones personalizadas: se ejecutan al guardar el formulario
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        # Verificar que la hora de fin sea posterior a la de inicio
        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError(
                    "La hora de fin debe ser posterior a la hora de inicio."
                )
        return cleaned_data
