#!/usr/bin/env python
# ============================================================
# SCRIPT DE DATOS DE PRUEBA - poblar_datos.py
# Ejecuta este script UNA vez después de las migraciones para
# llenar la base de datos con información de ejemplo.
# Uso: python manage.py shell < poblar_datos.py
#      O:  python poblar_datos.py (si configuras el entorno)
# ============================================================

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reservas.models import (
    Usuario, Rol, UsuarioRol, Complejo, TipoCancha,
    Cancha, EstadoReserva, MetodoPago, EstadoPago
)

print("Creando datos de prueba...")

# Roles
admin_rol, _ = Rol.objects.get_or_create(nombre_rol='Administrador')
cliente_rol, _ = Rol.objects.get_or_create(nombre_rol='Cliente')
print("✓ Roles creados")

# Estados de reserva
for estado, desc in [
    ('Pendiente', 'Reserva en espera de confirmación'),
    ('Confirmada', 'Reserva confirmada y activa'),
    ('Cancelada', 'Reserva cancelada'),
    ('Completada', 'Reserva completada exitosamente'),
]:
    EstadoReserva.objects.get_or_create(estado=estado, defaults={'descripcion': desc})
print("✓ Estados de reserva creados")

# Métodos de pago
for nombre, desc in [
    ('Efectivo', 'Pago en efectivo en el complejo'),
    ('Tarjeta de Crédito', 'Visa, Mastercard, etc.'),
    ('Transferencia Bancaria', 'PSE o transferencia directa'),
    ('Nequi', 'Pago por Nequi'),
]:
    MetodoPago.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
print("✓ Métodos de pago creados")

# Estados de pago
for estado, desc in [
    ('Pendiente', 'Pago no realizado aún'),
    ('Pagado', 'Pago recibido y confirmado'),
    ('Rechazado', 'Pago no procesado'),
    ('Reembolsado', 'Pago devuelto al cliente'),
]:
    EstadoPago.objects.get_or_create(estado=estado, defaults={'descripcion': desc})
print("✓ Estados de pago creados")

# Tipos de canchas
for nombre, desc in [
    ('Fútbol 11', 'Cancha de fútbol para 22 jugadores'),
    ('Fútbol 5', 'Microfútbol para 10 jugadores'),
    ('Baloncesto', 'Cancha de baloncesto reglamentaria'),
    ('Tenis', 'Cancha de tenis individual o dobles'),
    ('Pádel', 'Cancha de pádel'),
    ('Voleibol', 'Cancha de voleibol'),
]:
    TipoCancha.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
print("✓ Tipos de cancha creados")

# Superusuario admin
if not Usuario.objects.filter(username='admin').exists():
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@sportfield.com',
        password='admin123',
        first_name='Administrador',
        last_name='Sistema',
    )
    UsuarioRol.objects.create(usuario=admin, rol=admin_rol)
    print("✓ Admin creado (usuario: admin, clave: admin123)")

# Usuario de prueba
if not Usuario.objects.filter(username='juan').exists():
    juan = Usuario.objects.create_user(
        username='juan',
        email='juan@ejemplo.com',
        password='juan1234',
        first_name='Juan',
        last_name='Pérez',
        telefono='3001234567'
    )
    UsuarioRol.objects.create(usuario=juan, rol=cliente_rol)
    print("✓ Usuario juan creado (clave: juan1234)")

    # Complejo y canchas de ejemplo
    admin_user = Usuario.objects.get(username='admin')
    complejo1 = Complejo.objects.create(
        nombre_com='Complejo Deportivo Norte',
        ubicacion_com='Av. Norte #45-20, Cúcuta',
        id_usuario=admin_user
    )
    complejo2 = Complejo.objects.create(
        nombre_com='Canchas El Parque',
        ubicacion_com='Calle 10 #8-30, Cúcuta',
        id_usuario=admin_user
    )

    futbol5 = TipoCancha.objects.get(nombre='Fútbol 5')
    futbol11 = TipoCancha.objects.get(nombre='Fútbol 11')
    basket = TipoCancha.objects.get(nombre='Baloncesto')

    Cancha.objects.create(nombre_cancha='Cancha A', id_complejo=complejo1, id_tipo_can=futbol5, capacidad_can=10, precio_hora=50000, descripcion='Cancha sintética techada')
    Cancha.objects.create(nombre_cancha='Cancha B', id_complejo=complejo1, id_tipo_can=futbol5, capacidad_can=10, precio_hora=45000)
    Cancha.objects.create(nombre_cancha='Cancha Principal', id_complejo=complejo1, id_tipo_can=futbol11, capacidad_can=22, precio_hora=120000, descripcion='Cancha natural gramado')
    Cancha.objects.create(nombre_cancha='Cancha Basket 1', id_complejo=complejo2, id_tipo_can=basket, capacidad_can=12, precio_hora=35000)
    Cancha.objects.create(nombre_cancha='Cancha Fútbol C', id_complejo=complejo2, id_tipo_can=futbol5, capacidad_can=10, precio_hora=40000)
    print("✓ Complejos y canchas de prueba creados")

print("\n✅ ¡Base de datos lista! Ingresa en: http://127.0.0.1:8000/")
print("   Admin: http://127.0.0.1:8000/admin/ (admin / admin123)")
