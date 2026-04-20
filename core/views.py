from datetime import date

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CanchaForm,
    CanchaDisponibilidadForm,
    ComplejoForm,
    EstadoReservaRapidoForm,
    LoginForm,
    PagoClienteForm,
    PagoForm,
    ReservaClienteForm,
    ReservaForm,
    TipoCanchaForm,
)
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


def _usuario_activo(request):
    usuario_id = request.session.get('usuario_activo_id')
    if not usuario_id:
        return None
    return Usuario.objects.filter(pk=usuario_id).first()


def _roles_usuario(usuario):
    if not usuario:
        return set()
    return set(
        UsuarioRol.objects.filter(usuario=usuario).values_list('rol__nombre_rol', flat=True)
    )


def _contexto_base(request):
    usuario = _usuario_activo(request)
    roles = _roles_usuario(usuario)
    return {
        'usuario_activo': usuario,
        'es_admin': 'Administrador' in roles,
        'es_cliente': 'Cliente' in roles,
        'es_dueno': 'Dueno' in roles,
    }


def _redirigir_por_rol(roles):
    if 'Administrador' in roles:
        return 'gestion_inicio'
    if 'Dueno' in roles:
        return 'dueno_panel'
    return 'mi_panel'


def _requiere_login(request):
    if _usuario_activo(request):
        return None
    messages.info(request, 'Inicia sesion para continuar.')
    return redirect('login_usuario')


def _requiere_rol(request, permitidos):
    usuario = _usuario_activo(request)
    if not usuario:
        messages.info(request, 'Inicia sesion para continuar.')
        return redirect('login_usuario')
    roles = _roles_usuario(usuario)
    if roles.intersection(set(permitidos)):
        return None
    messages.error(request, 'No tienes permiso para entrar a esta seccion.')
    return redirect(_redirigir_por_rol(roles))


def portal_inicio(request):
    contexto = _contexto_base(request)
    contexto.update({
        'total_canchas': Cancha.objects.filter(disponible=True).count(),
        'total_complejos': Complejo.objects.count(),
        'reservas_hoy': Reserva.objects.filter(fecha=date.today()).count(),
        'total_reservas': Reserva.objects.count(),
        'total_usuarios': Usuario.objects.count(),
        'canchas_destacadas': Cancha.objects.select_related(
            'complejo', 'tipo_cancha'
        ).filter(disponible=True)[:3],
    })
    return render(request, 'portal/inicio.html', contexto)


def portal_canchas(request):
    # Catalogo principal para clientes: filtro por tipo, precio y disponibilidad.
    contexto = _contexto_base(request)
    tipo_id = request.GET.get('tipo')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    solo_disponibles = request.GET.get('solo_disponibles') == 'on'

    canchas = Cancha.objects.select_related('complejo', 'tipo_cancha').all()
    if tipo_id:
        canchas = canchas.filter(tipo_cancha_id=tipo_id)
    if precio_min:
        canchas = canchas.filter(precio_hora__gte=precio_min)
    if precio_max:
        canchas = canchas.filter(precio_hora__lte=precio_max)
    if solo_disponibles:
        canchas = canchas.filter(disponible=True)

    contexto.update({
        'canchas': canchas.order_by('precio_hora'),
        'tipos': TipoCancha.objects.all(),
        'filtro_tipo': tipo_id or '',
        'filtro_precio_min': precio_min or '',
        'filtro_precio_max': precio_max or '',
        'filtro_solo_disponibles': solo_disponibles,
    })
    return render(request, 'portal/canchas.html', contexto)


def portal_nosotros(request):
    # Pagina institucional para comunicar confianza de marca.
    contexto = _contexto_base(request)
    return render(request, 'portal/nosotros.html', contexto)


def login_usuario(request):
    # Login por email + contrasena guardada en Usuario.
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            usuario = Usuario.objects.filter(email=email).first()
            if not usuario:
                form.add_error(None, 'Credenciales invalidas.')
            else:
                # Compatibilidad: si la contrasena vieja estaba en texto plano, la migra a hash.
                coincide = check_password(contrasena, usuario.contrasena) or usuario.contrasena == contrasena
                if coincide:
                    if usuario.contrasena == contrasena:
                        usuario.contrasena = make_password(contrasena)
                        usuario.save(update_fields=['contrasena'])
                    request.session['usuario_activo_id'] = usuario.pk
                    roles = _roles_usuario(usuario)
                    messages.success(request, f'Bienvenido, {usuario.nombre}.')
                    return redirect(_redirigir_por_rol(roles))
                form.add_error(None, 'Credenciales invalidas.')
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form, **_contexto_base(request)})


def logout_usuario(request):
    request.session.pop('usuario_activo_id', None)
    messages.success(request, 'Sesion cerrada.')
    return redirect('portal_inicio')


def mi_panel(request):
    bloqueo = _requiere_rol(request, {'Cliente'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    reservas = Reserva.objects.select_related('cancha', 'estado_reserva').filter(
        usuario=usuario_activo
    ).order_by('-fecha', '-hora_inicio')
    pagos = Pago.objects.select_related('estado_pago', 'metodo_pago').filter(
        reserva__usuario=usuario_activo
    ).distinct().order_by('-fecha_pago')

    contexto = _contexto_base(request)
    contexto.update({'mis_reservas': reservas, 'mis_pagos': pagos})
    return render(request, 'portal/mi_panel.html', contexto)


def crear_reserva_cliente(request):
    bloqueo = _requiere_rol(request, {'Cliente'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    estado_inicial = EstadoReserva.objects.filter(estado__iexact='Pendiente').first()
    if not estado_inicial:
        messages.error(request, 'Crea al menos un estado llamado "Pendiente" en catalogos.')
        return redirect('mi_panel')

    cancha_preseleccionada = request.GET.get('cancha')
    if request.method == 'POST':
        form = ReservaClienteForm(request.POST)
        form.fields['cancha'].queryset = Cancha.objects.filter(disponible=True)
        cancha_preseleccionada = request.POST.get('cancha_preseleccionada') or cancha_preseleccionada
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = usuario_activo
            reserva.estado_reserva = estado_inicial
            reserva.save()
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('mi_panel')
    else:
        form = ReservaClienteForm()
        form.fields['cancha'].queryset = Cancha.objects.filter(disponible=True)
        if cancha_preseleccionada and form.fields['cancha'].queryset.filter(pk=cancha_preseleccionada).exists():
            form.initial['cancha'] = cancha_preseleccionada

    contexto = _contexto_base(request)
    contexto.update({'form': form, 'cancha_preseleccionada': cancha_preseleccionada})
    return render(request, 'portal/reservar.html', contexto)


def pagar_reserva_cliente(request, reserva_id):
    bloqueo = _requiere_rol(request, {'Cliente'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario=usuario_activo)
    estado_pago = EstadoPago.objects.filter(estado__iexact='Pagado').first()
    if not estado_pago:
        messages.error(request, 'No existe estado de pago "Pagado".')
        return redirect('mi_panel')

    if request.method == 'POST':
        form = PagoClienteForm(request.POST)
        if form.is_valid():
            pago = Pago.objects.create(
                monto=form.cleaned_data['monto_pago'],
                fecha_pago=date.today(),
                monto_pago=form.cleaned_data['monto_pago'],
                estado_pago=estado_pago,
                metodo_pago=form.cleaned_data['metodo_pago'],
            )
            reserva.pago = pago
            reserva.save(update_fields=['pago'])
            messages.success(request, 'Pago registrado y asociado a tu reserva.')
            return redirect('mi_panel')
    else:
        form = PagoClienteForm(initial={'monto_pago': 60000})

    contexto = _contexto_base(request)
    contexto.update({'form': form, 'reserva': reserva})
    return render(request, 'portal/pagar.html', contexto)


def dueno_panel(request):
    bloqueo = _requiere_rol(request, {'Dueno'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    canchas = Cancha.objects.select_related('complejo', 'tipo_cancha').filter(
        complejo__usuario=usuario_activo
    )
    reservas = Reserva.objects.select_related(
        'usuario', 'cancha', 'estado_reserva'
    ).filter(cancha__complejo__usuario=usuario_activo).order_by('-fecha', '-hora_inicio')

    contexto = _contexto_base(request)
    contexto.update({
        'canchas_dueno': canchas,
        'reservas_dueno': reservas,
        'estados_reserva': EstadoReserva.objects.all(),
    })
    return render(request, 'portal/dueno_panel.html', contexto)


def actualizar_disponibilidad_cancha(request, cancha_id):
    bloqueo = _requiere_rol(request, {'Dueno'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    cancha = get_object_or_404(Cancha, pk=cancha_id, complejo__usuario=usuario_activo)
    form = CanchaDisponibilidadForm(request.POST or None, instance=cancha)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Disponibilidad actualizada para {cancha.nombre_cancha}.')
    return redirect('dueno_panel')


def actualizar_estado_reserva(request, reserva_id):
    bloqueo = _requiere_rol(request, {'Dueno'})
    if bloqueo:
        return bloqueo

    usuario_activo = _usuario_activo(request)
    reserva = get_object_or_404(
        Reserva, pk=reserva_id, cancha__complejo__usuario=usuario_activo
    )
    form = EstadoReservaRapidoForm(request.POST or None, instance=reserva)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Estado actualizado para la reserva {reserva.pk}.')
    return redirect('dueno_panel')


def gestion_inicio(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo

    contexto = _contexto_base(request)
    contexto.update({
        'total_usuarios': Usuario.objects.count(),
        'total_complejos': Complejo.objects.count(),
        'total_canchas': Cancha.objects.count(),
        'total_reservas': Reserva.objects.count(),
        'ultimas_reservas': Reserva.objects.select_related(
            'usuario', 'cancha', 'estado_reserva'
        ).order_by('-fecha', '-hora_inicio')[:15],
    })
    return render(request, 'core/inicio.html', contexto)


def usuarios_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'titulo': 'Usuarios',
        'columnas': ['Nombre', 'Apellido', 'Email', 'Telefono'],
        'filas': Usuario.objects.all(),
        'tipo': 'usuarios',
    })
    return render(request, 'core/lista.html', contexto)


def complejos_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'titulo': 'Complejos',
        'columnas': ['Nombre', 'Ubicacion', 'Administrador'],
        'filas': Complejo.objects.select_related('usuario').all(),
        'tipo': 'complejos',
    })
    return render(request, 'core/lista.html', contexto)


def canchas_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'titulo': 'Canchas',
        'columnas': ['Nombre', 'Complejo', 'Tipo', 'Capacidad', 'Precio/Hora', 'Disponible'],
        'filas': Cancha.objects.select_related('complejo', 'tipo_cancha').all(),
        'tipo': 'canchas',
    })
    return render(request, 'core/lista.html', contexto)


def reservas_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'titulo': 'Historial completo de reservas',
        'columnas': ['Usuario', 'Cancha', 'Fecha', 'Horario', 'Estado'],
        'filas': Reserva.objects.select_related(
            'usuario', 'cancha', 'estado_reserva'
        ).all(),
        'tipo': 'reservas',
    })
    return render(request, 'core/lista.html', contexto)


def pagos_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'titulo': 'Historial completo de pagos',
        'columnas': ['Monto', 'Fecha', 'Monto pagado', 'Estado', 'Metodo'],
        'filas': Pago.objects.select_related('estado_pago', 'metodo_pago').all(),
        'tipo': 'pagos',
    })
    return render(request, 'core/lista.html', contexto)


def crear_reserva(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('reservas_lista')
    else:
        form = ReservaForm()
    return render(request, 'core/formulario.html', {'titulo': 'Nueva reserva', 'form': form, **_contexto_base(request)})


def crear_pago(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('pagos_lista')
    else:
        form = PagoForm()
    return render(request, 'core/formulario.html', {'titulo': 'Nuevo pago', 'form': form, **_contexto_base(request)})


def crear_complejo(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    if request.method == 'POST':
        form = ComplejoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complejo creado correctamente.')
            return redirect('complejos_lista')
    else:
        form = ComplejoForm()
    return render(request, 'core/formulario.html', {'titulo': 'Nuevo complejo', 'form': form, **_contexto_base(request)})


def crear_tipo_cancha(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    if request.method == 'POST':
        form = TipoCanchaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de cancha creado correctamente.')
            return redirect('catalogos_lista')
    else:
        form = TipoCanchaForm()
    return render(request, 'core/formulario.html', {'titulo': 'Nuevo tipo de cancha', 'form': form, **_contexto_base(request)})


def crear_cancha(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    if request.method == 'POST':
        form = CanchaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cancha creada correctamente.')
            return redirect('canchas_lista')
    else:
        form = CanchaForm()
    return render(request, 'core/formulario.html', {'titulo': 'Nueva cancha', 'form': form, **_contexto_base(request)})


def catalogos_lista(request):
    bloqueo = _requiere_rol(request, {'Administrador'})
    if bloqueo:
        return bloqueo
    contexto = _contexto_base(request)
    contexto.update({
        'roles': Rol.objects.all(),
        'usuarios_roles': UsuarioRol.objects.select_related('usuario', 'rol').all(),
        'tipos_canchas': TipoCancha.objects.all(),
        'estados_reserva': EstadoReserva.objects.all(),
        'estados_pago': EstadoPago.objects.all(),
        'metodos_pago': MetodoPago.objects.all(),
    })
    return render(request, 'core/catalogos.html', contexto)
