# ============================================================
# MODELOS DE BASE DE DATOS - reservas/models.py
# Cada clase aquí representa una tabla en la base de datos.
# Django crea las tablas automáticamente con "makemigrations"
# y "migrate". No necesitas escribir SQL manualmente.
# ============================================================

from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------------------------------------
# MODELO: Usuario
# Extiende el usuario base de Django para agregar campos
# extra como teléfono. Django ya maneja email, contraseña,
# nombre y apellido por defecto.
# -------------------------------------------------------
class Usuario(AbstractUser):
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# -------------------------------------------------------
# MODELO: Rol
# Define los roles del sistema: Administrador, Cliente, etc.
# -------------------------------------------------------
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Rol")

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre_rol


# -------------------------------------------------------
# MODELO: UsuarioRol (tabla intermedia muchos a muchos)
# Un usuario puede tener varios roles.
# -------------------------------------------------------
class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="roles_asignados")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name="usuarios_con_rol")

    class Meta:
        verbose_name = "Usuario - Rol"
        unique_together = ('usuario', 'rol')

    def __str__(self):
        return f"{self.usuario} -> {self.rol}"


# -------------------------------------------------------
# MODELO: Complejo
# Lugar físico que contiene las canchas.
# -------------------------------------------------------
class Complejo(models.Model):
    nombre_com = models.CharField(max_length=200, verbose_name="Nombre del Complejo")
    ubicacion_com = models.TextField(verbose_name="Ubicación")
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="complejos")

    class Meta:
        verbose_name = "Complejo"
        verbose_name_plural = "Complejos"

    def __str__(self):
        return self.nombre_com


# -------------------------------------------------------
# MODELO: TipoCancha
# Fútbol, Baloncesto, Tenis, Pádel, etc.
# -------------------------------------------------------
class TipoCancha(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Tipo de Cancha")
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Cancha"
        verbose_name_plural = "Tipos de Canchas"

    def __str__(self):
        return self.nombre


# -------------------------------------------------------
# MODELO: Cancha
# Una cancha pertenece a un Complejo y tiene un Tipo.
# -------------------------------------------------------
class Cancha(models.Model):
    id_complejo = models.ForeignKey(Complejo, on_delete=models.CASCADE, related_name="canchas")
    nombre_cancha = models.CharField(max_length=200, verbose_name="Nombre de la Cancha")
    capacidad_can = models.PositiveIntegerField(verbose_name="Capacidad")
    descripcion = models.TextField(blank=True)
    id_tipo_can = models.ForeignKey(TipoCancha, on_delete=models.SET_NULL, null=True, related_name="canchas")
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cancha"
        verbose_name_plural = "Canchas"

    def __str__(self):
        return f"{self.nombre_cancha} - {self.id_complejo.nombre_com}"


# -------------------------------------------------------
# MODELO: EstadoReserva
# Pendiente, Confirmada, Cancelada, Completada.
# -------------------------------------------------------
class EstadoReserva(models.Model):
    estado = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Estado de Reserva"

    def __str__(self):
        return self.estado


# -------------------------------------------------------
# MODELO: MetodoPago
# Efectivo, Tarjeta, Transferencia, etc.
# -------------------------------------------------------
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Método de Pago"

    def __str__(self):
        return self.nombre


# -------------------------------------------------------
# MODELO: EstadoPago
# Pendiente, Pagado, Rechazado, Reembolsado.
# -------------------------------------------------------
class EstadoPago(models.Model):
    estado = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Estado de Pago"

    def __str__(self):
        return self.estado


# -------------------------------------------------------
# MODELO: Pago
# Registra el pago asociado a una reserva.
# -------------------------------------------------------
class Pago(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total")
    fecha_pago = models.DateField(verbose_name="Fecha de Pago")
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    id_estado_pago = models.ForeignKey(EstadoPago, on_delete=models.SET_NULL, null=True, related_name="pagos")
    id_metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True, related_name="pagos")

    class Meta:
        verbose_name = "Pago"

    def __str__(self):
        return f"Pago #{self.pk} - ${self.monto_pago}"


# -------------------------------------------------------
# MODELO: Reserva - El corazón del sistema.
# Conecta Usuario + Cancha + Pago.
# -------------------------------------------------------
class Reserva(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    id_cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name="reservas")
    id_pagos = models.OneToOneField(Pago, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserva")
    fecha = models.DateField(verbose_name="Fecha de Reserva")
    hora_inicio = models.TimeField(verbose_name="Hora Inicio")
    hora_fin = models.TimeField(verbose_name="Hora Fin")
    id_estado_res = models.ForeignKey(EstadoReserva, on_delete=models.SET_NULL, null=True, related_name="reservas")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Reserva #{self.pk} - {self.id_cancha} - {self.fecha}"
