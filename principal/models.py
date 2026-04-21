# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cancha(models.Model):
    id_cancha = models.AutoField(db_column='Id_Cancha', primary_key=True)  # Field name made lowercase.
    nombre_cancha = models.CharField(db_column='Nombre_Cancha', max_length=20)  # Field name made lowercase.
    capacidad_cancha = models.IntegerField(db_column='Capacidad_Cancha')  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=10, decimal_places=2)  # Field name made lowercase.
    id_complejo = models.ForeignKey('Complejo', models.DO_NOTHING, db_column='Id_Complejo')  # Field name made lowercase.
    id_tipo_cancha = models.ForeignKey('TipoCancha', models.DO_NOTHING, db_column='Id_Tipo_Cancha')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cancha'


class Complejo(models.Model):
    id_complejo = models.AutoField(db_column='Id_Complejo', primary_key=True)  # Field name made lowercase.
    nombre_complejo = models.CharField(db_column='Nombre_Complejo', max_length=100)  # Field name made lowercase.
    ubicacion_complejo = models.CharField(db_column='Ubicacion_Complejo', max_length=200)  # Field name made lowercase.
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Id_Usuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complejo'


class EstadoPago(models.Model):
    id_estado_pago = models.AutoField(db_column='Id_Estado_Pago', primary_key=True)  # Field name made lowercase.
    estado_pago = models.CharField(db_column='Estado_Pago', max_length=50)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estado_pago'


class EstadoReserva(models.Model):
    id_estado_reserva = models.AutoField(db_column='Id_Estado_Reserva', primary_key=True)  # Field name made lowercase.
    estado_reserva = models.CharField(db_column='Estado_Reserva', max_length=50)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estado_reserva'


class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(db_column='Id_Metodo_Pago', primary_key=True)  # Field name made lowercase.
    nombre_metodo = models.CharField(db_column='Nombre_Metodo', max_length=50)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'metodo_pago'


class Pagos(models.Model):
    id_pago = models.AutoField(db_column='Id_Pago', primary_key=True)  # Field name made lowercase.
    monto_pago = models.DecimalField(db_column='Monto_Pago', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fecha_pago = models.DateField(db_column='Fecha_Pago')  # Field name made lowercase.
    id_estado_pago = models.ForeignKey(EstadoPago, models.DO_NOTHING, db_column='Id_Estado_Pago')  # Field name made lowercase.
    id_metodo_pago = models.ForeignKey(MetodoPago, models.DO_NOTHING, db_column='Id_Metodo_pago')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pagos'


class Reserva(models.Model):
    id_reserva = models.AutoField(db_column='Id_Reserva', primary_key=True)  # Field name made lowercase.
    fecha_reserva = models.DateField(db_column='Fecha_Reserva')  # Field name made lowercase.
    hora_inicio = models.TimeField(db_column='Hora_Inicio')  # Field name made lowercase.
    hora_fin = models.TimeField(db_column='Hora_Fin')  # Field name made lowercase.
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Id_Usuario')  # Field name made lowercase.
    id_cancha = models.ForeignKey(Cancha, models.DO_NOTHING, db_column='Id_Cancha')  # Field name made lowercase.
    id_pago = models.ForeignKey(Pagos, models.DO_NOTHING, db_column='Id_Pago')  # Field name made lowercase.
    id_estado_reserva = models.ForeignKey(EstadoReserva, models.DO_NOTHING, db_column='Id_Estado_Reserva')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reserva'


class Rol(models.Model):
    id_rol = models.AutoField(db_column='Id_Rol', primary_key=True)  # Field name made lowercase.
    nombre_rol = models.CharField(db_column='Nombre_Rol', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rol'


class TipoCancha(models.Model):
    id_tipo_cancha = models.AutoField(db_column='Id_Tipo_Cancha', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipo_cancha'


class Usuario(models.Model):
    id_usuario = models.IntegerField(db_column='Id_Usuario', primary_key=True)  # Field name made lowercase.
    nombre_usu = models.CharField(db_column='Nombre_Usu', max_length=20)  # Field name made lowercase.
    apellido_usu = models.CharField(db_column='Apellido_Usu', max_length=20)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contraseña', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'


class UsuarioRol(models.Model):
    id_usuario_rol = models.AutoField(db_column='Id_Usuario_Rol', primary_key=True)  # Field name made lowercase.
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Id_Usuario')  # Field name made lowercase.
    id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='Id_Rol')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario_rol'
