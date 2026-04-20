# ============================================================
# PANEL DE ADMINISTRACIÓN - reservas/admin.py
# Django genera automáticamente un panel de admin en /admin/
# Solo debes registrar aquí tus modelos y Django hace el resto.
# ============================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Rol, UsuarioRol, Complejo, TipoCancha,
    Cancha, EstadoReserva, MetodoPago, EstadoPago, Pago, Reserva
)

# -------------------------------------------------------
# Configuración del admin para Usuario personalizado
# -------------------------------------------------------
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos extra que aparecen en la vista de detalle del admin
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('telefono',)}),
    )
    list_display = ['username', 'first_name', 'last_name', 'email', 'telefono', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']


# -------------------------------------------------------
# Registros simples: así aparecen en el panel /admin/
# -------------------------------------------------------
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre_rol']


@admin.register(Complejo)
class ComplejoAdmin(admin.ModelAdmin):
    list_display = ['nombre_com', 'ubicacion_com', 'id_usuario']
    search_fields = ['nombre_com', 'ubicacion_com']


@admin.register(TipoCancha)
class TipoCanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']


@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre_cancha', 'id_complejo', 'id_tipo_can', 'capacidad_can', 'precio_hora', 'activa']
    list_filter = ['activa', 'id_tipo_can', 'id_complejo']  # Filtros en la barra lateral
    search_fields = ['nombre_cancha']


@admin.register(EstadoReserva)
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ['estado', 'descripcion']


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']


@admin.register(EstadoPago)
class EstadoPagoAdmin(admin.ModelAdmin):
    list_display = ['estado', 'descripcion']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'monto', 'monto_pago', 'fecha_pago', 'id_estado_pago', 'id_metodo_pago']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'id_usuario', 'id_cancha', 'fecha', 'hora_inicio', 'hora_fin', 'id_estado_res']
    list_filter = ['id_estado_res', 'fecha']  # Filtro por estado y fecha
    search_fields = ['id_usuario__username', 'id_cancha__nombre_cancha']
    date_hierarchy = 'fecha'  # Navegación por fechas en la parte superior
