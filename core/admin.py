from django.contrib import admin

from .models import (
    Cancha,
    Complejo,
    EstadoPago,
    EstadoReserva,
    MetodoPago,
    Pago,
    Reserva,
    Rol,
    TipoCancha,
    Usuario,
    UsuarioRol,
)

# Registrar modelos para poder gestionarlos desde /admin.
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(UsuarioRol)
admin.site.register(Complejo)
admin.site.register(TipoCancha)
admin.site.register(Cancha)
admin.site.register(EstadoReserva)
admin.site.register(MetodoPago)
admin.site.register(EstadoPago)
admin.site.register(Pago)
admin.site.register(Reserva)
