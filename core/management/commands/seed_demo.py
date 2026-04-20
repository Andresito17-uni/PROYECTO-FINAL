from datetime import date, time
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from core.models import (
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


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para ver la interfaz con contenido.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creando datos demo...'))

        # 1) Catalogos base
        rol_admin, _ = Rol.objects.get_or_create(nombre_rol='Administrador')
        rol_cliente, _ = Rol.objects.get_or_create(nombre_rol='Cliente')
        rol_dueno, _ = Rol.objects.get_or_create(nombre_rol='Dueno')

        tipo_futbol, _ = TipoCancha.objects.get_or_create(
            nombre='Futbol 5', defaults={'descripcion': 'Cancha sintetica'}
        )
        tipo_tenis, _ = TipoCancha.objects.get_or_create(
            nombre='Tenis', defaults={'descripcion': 'Cancha de tenis'}
        )

        estado_res_pend, _ = EstadoReserva.objects.get_or_create(
            estado='Pendiente', defaults={'descripcion': 'Reserva en validacion'}
        )
        estado_res_conf, _ = EstadoReserva.objects.get_or_create(
            estado='Confirmada', defaults={'descripcion': 'Reserva aprobada'}
        )

        metodo_nequi, _ = MetodoPago.objects.get_or_create(
            nombre='Nequi', defaults={'descripcion': 'Pago por app'}
        )
        metodo_efectivo, _ = MetodoPago.objects.get_or_create(
            nombre='Efectivo', defaults={'descripcion': 'Pago en caja'}
        )

        estado_pago_ok, _ = EstadoPago.objects.get_or_create(
            estado='Pagado', defaults={'descripcion': 'Pago aprobado'}
        )
        estado_pago_pen, _ = EstadoPago.objects.get_or_create(
            estado='Pendiente', defaults={'descripcion': 'Pago por confirmar'}
        )

        # 2) Usuarios de ejemplo
        admin_user, _ = Usuario.objects.get_or_create(
            email='admin@reservarr.com',
            defaults={
                'nombre': 'Ana',
                'apellido': 'Admin',
                'contrasena': '123456',
                'telefono': '300000001',
            },
        )
        cliente_1, _ = Usuario.objects.get_or_create(
            email='carlos@correo.com',
            defaults={
                'nombre': 'Carlos',
                'apellido': 'Lopez',
                'contrasena': '123456',
                'telefono': '300000002',
            },
        )
        cliente_2, _ = Usuario.objects.get_or_create(
            email='maria@correo.com',
            defaults={
                'nombre': 'Maria',
                'apellido': 'Rojas',
                'contrasena': '123456',
                'telefono': '300000003',
            },
        )
        dueno_1, _ = Usuario.objects.get_or_create(
            email='dueno@complejo.com',
            defaults={
                'nombre': 'Diego',
                'apellido': 'Dueno',
                'contrasena': '123456',
                'telefono': '300000004',
            },
        )

        # Convertimos a hash por seguridad y para login real.
        for usr in [admin_user, cliente_1, cliente_2, dueno_1]:
            usr.contrasena = make_password('123456')
            usr.save(update_fields=['contrasena'])

        UsuarioRol.objects.get_or_create(usuario=admin_user, rol=rol_admin)
        UsuarioRol.objects.get_or_create(usuario=cliente_1, rol=rol_cliente)
        UsuarioRol.objects.get_or_create(usuario=cliente_2, rol=rol_cliente)
        UsuarioRol.objects.get_or_create(usuario=dueno_1, rol=rol_dueno)

        # 3) Complejos y canchas
        complejo_1, _ = Complejo.objects.get_or_create(
            nombre_com='Complejo Norte',
            defaults={'ubicacion_com': 'Calle 100 # 20-30', 'usuario': admin_user},
        )
        complejo_2, _ = Complejo.objects.get_or_create(
            nombre_com='Complejo Sur',
            defaults={'ubicacion_com': 'Av. Sur # 45-10', 'usuario': dueno_1},
        )
        if complejo_2.usuario_id != dueno_1.id:
            complejo_2.usuario = dueno_1
            complejo_2.save(update_fields=['usuario'])

        cancha_1, _ = Cancha.objects.get_or_create(
            nombre_cancha='Cancha A',
            defaults={
                'complejo': complejo_1,
                'capacidad_can': 10,
                'precio_hora': Decimal('80000.00'),
                'descripcion': 'Iluminacion nocturna',
                'tipo_cancha': tipo_futbol,
            },
        )
        cancha_2, _ = Cancha.objects.get_or_create(
            nombre_cancha='Cancha B',
            defaults={
                'complejo': complejo_2,
                'capacidad_can': 4,
                'precio_hora': Decimal('50000.00'),
                'descripcion': 'Superficie dura',
                'tipo_cancha': tipo_tenis,
            },
        )
        if cancha_1.precio_hora == 0:
            cancha_1.precio_hora = Decimal('80000.00')
            cancha_1.save(update_fields=['precio_hora'])
        if cancha_2.precio_hora == 0:
            cancha_2.precio_hora = Decimal('50000.00')
            cancha_2.save(update_fields=['precio_hora'])

        # 4) Pagos y reservas
        pago_1, _ = Pago.objects.get_or_create(
            monto=Decimal('80000.00'),
            fecha_pago=date.today(),
            monto_pago=Decimal('80000.00'),
            estado_pago=estado_pago_ok,
            metodo_pago=metodo_nequi,
        )
        pago_2, _ = Pago.objects.get_or_create(
            monto=Decimal('50000.00'),
            fecha_pago=date.today(),
            monto_pago=Decimal('50000.00'),
            estado_pago=estado_pago_pen,
            metodo_pago=metodo_efectivo,
        )

        Reserva.objects.get_or_create(
            usuario=cliente_1,
            cancha=cancha_1,
            pago=pago_1,
            fecha=date.today(),
            hora_inicio=time(18, 0),
            hora_fin=time(19, 0),
            estado_reserva=estado_res_conf,
        )
        Reserva.objects.get_or_create(
            usuario=cliente_2,
            cancha=cancha_2,
            pago=pago_2,
            fecha=date.today(),
            hora_inicio=time(16, 0),
            hora_fin=time(17, 0),
            estado_reserva=estado_res_pend,
        )

        self.stdout.write(self.style.SUCCESS('Datos demo creados correctamente.'))
