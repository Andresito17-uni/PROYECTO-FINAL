from django.contrib import admin

# Importamos todas las clases de tu archivo models.py
from .models import (
    Cancha, 
    Complejo, 
    EstadoPago, 
    EstadoReserva, 
    MetodoPago, 
    Pagos, 
    Reserva, 
    Rol, 
    TipoCancha, 
    Usuario, 
    UsuarioRol
)

# Declaramos cada tabla para que el panel de administrador las muestre
admin.site.register(Cancha)
admin.site.register(Complejo)
admin.site.register(EstadoPago)
admin.site.register(EstadoReserva)
admin.site.register(MetodoPago)
admin.site.register(Pagos)
admin.site.register(Reserva)
admin.site.register(Rol)
admin.site.register(TipoCancha)
admin.site.register(Usuario)
admin.site.register(UsuarioRol)