from django import forms

from .models import Cancha, Complejo, MetodoPago, Pago, Reserva, TipoCancha, Usuario


class ReservaForm(forms.ModelForm):
    # Formulario para crear reservas desde la interfaz web.
    class Meta:
        model = Reserva
        fields = [
            'usuario',
            'cancha',
            'pago',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'estado_reserva',
        ]
        widgets = {
            # Widgets HTML5 para mejor experiencia visual.
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        # Aplicamos clases de Bootstrap para mejorar la presentacion.
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
            campo.widget.attrs['class'] = css_class


class PagoForm(forms.ModelForm):
    # Formulario para registrar pagos.
    class Meta:
        model = Pago
        fields = ['monto', 'fecha_pago', 'monto_pago', 'estado_pago', 'metodo_pago']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
            campo.widget.attrs['class'] = css_class


class ReservaClienteForm(forms.ModelForm):
    # Formulario para clientes: no permite elegir usuario ni estado manualmente.
    class Meta:
        model = Reserva
        fields = ['cancha', 'fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
            campo.widget.attrs['class'] = css_class


class CambiarUsuarioForm(forms.Form):
    # Selector simple para simular login/cambio de usuario.
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label='Selecciona un usuario',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs['class'] = 'form-select'


class LoginForm(forms.Form):
    # Login basico usando email + contrasena del modelo Usuario.
    email = forms.EmailField(label='Correo')
    contrasena = forms.CharField(label='Contrasena', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['contrasena'].widget.attrs['class'] = 'form-control'


class ComplejoForm(forms.ModelForm):
    # Formulario para que admin cree nuevos complejos.
    class Meta:
        model = Complejo
        fields = ['nombre_com', 'ubicacion_com', 'usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
            campo.widget.attrs['class'] = css_class


class TipoCanchaForm(forms.ModelForm):
    # Formulario para registrar nuevos tipos de cancha.
    class Meta:
        model = TipoCancha
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
            campo.widget.attrs['class'] = css_class


class CanchaForm(forms.ModelForm):
    # Formulario para crear nuevas canchas en complejos existentes.
    class Meta:
        model = Cancha
        fields = [
            'complejo',
            'nombre_cancha',
            'capacidad_can',
            'precio_hora',
            'descripcion',
            'tipo_cancha',
            'disponible',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if nombre == 'disponible':
                campo.widget.attrs['class'] = 'form-check-input'
            else:
                css_class = 'form-select' if hasattr(campo.widget, 'choices') else 'form-control'
                campo.widget.attrs['class'] = css_class


class CanchaDisponibilidadForm(forms.ModelForm):
    # El dueno puede cambiar disponibilidad sin editar toda la cancha.
    class Meta:
        model = Cancha
        fields = ['disponible']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disponible'].widget.attrs['class'] = 'form-check-input'


class EstadoReservaRapidoForm(forms.ModelForm):
    # El dueno confirma/cancela desde su panel.
    class Meta:
        model = Reserva
        fields = ['estado_reserva']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado_reserva'].widget.attrs['class'] = 'form-select'


class PagoClienteForm(forms.Form):
    # Cliente registra pago para una reserva especifica.
    metodo_pago = forms.ModelChoiceField(queryset=MetodoPago.objects.all(), empty_label=None)
    monto_pago = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['metodo_pago'].widget.attrs['class'] = 'form-select'
        self.fields['monto_pago'].widget.attrs['class'] = 'form-control'
