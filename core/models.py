from django.db import models


class Usuario(models.Model):
    # Datos base de cada usuario del sistema.
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Rol(models.Model):
    # Roles posibles: admin, cliente, encargado, etc.
    nombre_rol = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol


class UsuarioRol(models.Model):
    # Tabla puente para relacion muchos usuarios con muchos roles.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Usuario-Rol'
        verbose_name_plural = 'Usuarios-Roles'
        unique_together = ('usuario', 'rol')

    def __str__(self):
        return f'{self.usuario} -> {self.rol}'


class Complejo(models.Model):
    # Sede o complejo deportivo que agrupa canchas.
    nombre_com = models.CharField(max_length=100)
    ubicacion_com = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Complejo'
        verbose_name_plural = 'Complejos'

    def __str__(self):
        return self.nombre_com


class TipoCancha(models.Model):
    # Catalogo de tipos de cancha (futbol, tenis, etc.).
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Tipo de cancha'
        verbose_name_plural = 'Tipos de cancha'

    def __str__(self):
        return self.nombre


class Cancha(models.Model):
    # Cancha fisica reservable.
    complejo = models.ForeignKey(Complejo, on_delete=models.PROTECT)
    nombre_cancha = models.CharField(max_length=100)
    capacidad_can = models.PositiveIntegerField()
    # Precio de reserva por hora para filtrar y mostrar al cliente.
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion = models.TextField(blank=True)
    tipo_cancha = models.ForeignKey(TipoCancha, on_delete=models.PROTECT)
    # Permite al dueno bloquear/desbloquear reservas en esta cancha.
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'

    def __str__(self):
        return self.nombre_cancha


class EstadoReserva(models.Model):
    # Estado de la reserva: pendiente, confirmada, cancelada, etc.
    estado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Estado de reserva'
        verbose_name_plural = 'Estados de reserva'

    def __str__(self):
        return self.estado


class MetodoPago(models.Model):
    # Metodo de pago disponible para los usuarios.
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Metodo de pago'
        verbose_name_plural = 'Metodos de pago'

    def __str__(self):
        return self.nombre


class EstadoPago(models.Model):
    # Estado del pago: pagado, pendiente, rechazado, etc.
    estado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Estado de pago'
        verbose_name_plural = 'Estados de pago'

    def __str__(self):
        return self.estado


class Pago(models.Model):
    # Registro monetario asociado a una reserva.
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f'Pago #{self.pk} - {self.monto_pago}'


class Reserva(models.Model):
    # Reserva principal que une usuario, cancha y pago.
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    cancha = models.ForeignKey(Cancha, on_delete=models.PROTECT)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva #{self.pk} - {self.usuario}'
