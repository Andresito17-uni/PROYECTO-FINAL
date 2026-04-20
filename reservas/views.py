# ============================================================
# VISTAS - reservas/views.py
# Las vistas son funciones Python que reciben una solicitud (request)
# del navegador y devuelven una respuesta (HTML, redirect, etc.)
# Es la lógica de negocio de la aplicación.
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count
from .models import Usuario, Complejo, Cancha, Reserva, EstadoReserva, Pago, EstadoPago, MetodoPago
from .forms import RegistroForm, LoginForm, ComplejoForm, CanchaForm, ReservaForm
import datetime


# -------------------------------------------------------
# VISTA: Página de inicio
# Si el usuario ya inició sesión, va al dashboard.
# Si no, va al login.
# -------------------------------------------------------
def inicio(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


# -------------------------------------------------------
# VISTA: Login personalizado
# Usamos una clase basada en LoginView de Django
# -------------------------------------------------------
class CustomLoginView(LoginView):
    form_class = LoginForm          # Nuestro formulario personalizado
    template_name = 'auth/login.html'  # Template que renderiza

    def get_success_url(self):
        # Después del login exitoso, va al dashboard
        return '/dashboard/'


# -------------------------------------------------------
# VISTA: Registro de nuevo usuario
# -------------------------------------------------------
def registro(request):
    if request.method == 'POST':
        # Si el formulario fue enviado (método POST)
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Si los datos son válidos, guardamos el usuario
            usuario = form.save(commit=False)
            usuario.telefono = form.cleaned_data.get('telefono')
            usuario.save()
            # Iniciamos sesión automáticamente después del registro
            login(request, usuario)
            messages.success(request, f'¡Bienvenido, {usuario.first_name}! Tu cuenta fue creada.')
            return redirect('dashboard')
    else:
        # Si es GET, mostramos el formulario vacío
        form = RegistroForm()

    return render(request, 'auth/registro.html', {'form': form})


# -------------------------------------------------------
# VISTA: Dashboard principal
# @login_required → Si no hay sesión, redirige al login
# -------------------------------------------------------
@login_required
def dashboard(request):
    # Contamos los datos para mostrar estadísticas
    total_reservas = Reserva.objects.filter(id_usuario=request.user).count()
    total_canchas = Cancha.objects.filter(activa=True).count()
    total_complejos = Complejo.objects.count()

    # Últimas 5 reservas del usuario actual
    mis_reservas = Reserva.objects.filter(
        id_usuario=request.user
    ).select_related('id_cancha', 'id_estado_res')[:5]

    # Contexto: diccionario con datos que enviamos al template HTML
    contexto = {
        'total_reservas': total_reservas,
        'total_canchas': total_canchas,
        'total_complejos': total_complejos,
        'mis_reservas': mis_reservas,
        'usuario': request.user,
    }
    return render(request, 'dashboard.html', contexto)


# -------------------------------------------------------
# VISTAS: COMPLEJOS
# -------------------------------------------------------

@login_required
def lista_complejos(request):
    # Trae todos los complejos con sus canchas relacionadas
    complejos = Complejo.objects.annotate(num_canchas=Count('canchas')).all()
    return render(request, 'complejos/lista.html', {'complejos': complejos})


@login_required
def crear_complejo(request):
    if request.method == 'POST':
        form = ComplejoForm(request.POST)
        if form.is_valid():
            complejo = form.save(commit=False)
            # Asignamos el usuario actual como propietario del complejo
            complejo.id_usuario = request.user
            complejo.save()
            messages.success(request, 'Complejo creado exitosamente.')
            return redirect('lista_complejos')
    else:
        form = ComplejoForm()
    return render(request, 'complejos/formulario.html', {'form': form, 'titulo': 'Nuevo Complejo'})


@login_required
def editar_complejo(request, pk):
    # get_object_or_404: busca el complejo o devuelve error 404 si no existe
    complejo = get_object_or_404(Complejo, pk=pk)
    if request.method == 'POST':
        form = ComplejoForm(request.POST, instance=complejo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complejo actualizado.')
            return redirect('lista_complejos')
    else:
        form = ComplejoForm(instance=complejo)
    return render(request, 'complejos/formulario.html', {'form': form, 'titulo': 'Editar Complejo'})


@login_required
def eliminar_complejo(request, pk):
    complejo = get_object_or_404(Complejo, pk=pk)
    if request.method == 'POST':
        complejo.delete()
        messages.success(request, 'Complejo eliminado.')
        return redirect('lista_complejos')
    return render(request, 'complejos/confirmar_eliminar.html', {'objeto': complejo})


# -------------------------------------------------------
# VISTAS: CANCHAS
# -------------------------------------------------------

@login_required
def lista_canchas(request):
    canchas = Cancha.objects.select_related('id_complejo', 'id_tipo_can').all()
    return render(request, 'canchas/lista.html', {'canchas': canchas})


@login_required
def crear_cancha(request):
    if request.method == 'POST':
        form = CanchaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cancha creada exitosamente.')
            return redirect('lista_canchas')
    else:
        form = CanchaForm()
    return render(request, 'canchas/formulario.html', {'form': form, 'titulo': 'Nueva Cancha'})


@login_required
def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        form = CanchaForm(request.POST, instance=cancha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cancha actualizada.')
            return redirect('lista_canchas')
    else:
        form = CanchaForm(instance=cancha)
    return render(request, 'canchas/formulario.html', {'form': form, 'titulo': 'Editar Cancha'})


@login_required
def eliminar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        cancha.delete()
        messages.success(request, 'Cancha eliminada.')
        return redirect('lista_canchas')
    return render(request, 'canchas/confirmar_eliminar.html', {'objeto': cancha})


# -------------------------------------------------------
# VISTAS: RESERVAS
# -------------------------------------------------------

@login_required
def lista_reservas(request):
    # Si es admin, ve todas las reservas. Si no, solo las suyas.
    if request.user.is_staff:
        reservas = Reserva.objects.select_related(
            'id_usuario', 'id_cancha', 'id_estado_res'
        ).all()
    else:
        reservas = Reserva.objects.filter(
            id_usuario=request.user
        ).select_related('id_cancha', 'id_estado_res')

    return render(request, 'reservas/lista.html', {'reservas': reservas})


@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.id_usuario = request.user

            # Asignamos el estado "Pendiente" por defecto
            estado_pendiente, _ = EstadoReserva.objects.get_or_create(
                estado='Pendiente',
                defaults={'descripcion': 'Reserva en espera de confirmación'}
            )
            reserva.id_estado_res = estado_pendiente
            reserva.save()
            messages.success(request, '¡Reserva creada! Está pendiente de confirmación.')
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/formulario.html', {'form': form})


@login_required
def detalle_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    return render(request, 'reservas/detalle.html', {'reserva': reserva})


@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, id_usuario=request.user)
    if request.method == 'POST':
        estado_cancelada, _ = EstadoReserva.objects.get_or_create(
            estado='Cancelada',
            defaults={'descripcion': 'Reserva cancelada por el usuario'}
        )
        reserva.id_estado_res = estado_cancelada
        reserva.save()
        messages.warning(request, 'Reserva cancelada.')
        return redirect('lista_reservas')
    return render(request, 'reservas/confirmar_cancelar.html', {'reserva': reserva})


@login_required
def lista_usuarios(request):
    # Solo los administradores pueden ver la lista de usuarios
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta sección.')
        return redirect('dashboard')
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})
