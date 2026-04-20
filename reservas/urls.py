# ============================================================
# URLs DE LA APP - reservas/urls.py
# Aquí se definen todas las rutas de nuestra aplicación.
# path('ruta/', vista, name='nombre_url')
# ============================================================

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Importamos nuestras vistas

urlpatterns = [

    # -------------------------------------------------------
    # AUTENTICACIÓN
    # -------------------------------------------------------
    # Página de inicio → redirige al login si no hay sesión
    path('', views.inicio, name='inicio'),

    # Login: muestra el formulario de entrada
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Logout: cierra la sesión y redirige al login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registro de nuevo usuario
    path('registro/', views.registro, name='registro'),

    # -------------------------------------------------------
    # DASHBOARD PRINCIPAL (requiere login)
    # -------------------------------------------------------
    path('dashboard/', views.dashboard, name='dashboard'),

    # -------------------------------------------------------
    # COMPLEJOS (CRUD completo)
    # CRUD = Create, Read, Update, Delete
    # -------------------------------------------------------
    path('complejos/', views.lista_complejos, name='lista_complejos'),
    path('complejos/nuevo/', views.crear_complejo, name='crear_complejo'),
    path('complejos/<int:pk>/editar/', views.editar_complejo, name='editar_complejo'),
    path('complejos/<int:pk>/eliminar/', views.eliminar_complejo, name='eliminar_complejo'),

    # -------------------------------------------------------
    # CANCHAS (CRUD completo)
    # -------------------------------------------------------
    path('canchas/', views.lista_canchas, name='lista_canchas'),
    path('canchas/nueva/', views.crear_cancha, name='crear_cancha'),
    path('canchas/<int:pk>/editar/', views.editar_cancha, name='editar_cancha'),
    path('canchas/<int:pk>/eliminar/', views.eliminar_cancha, name='eliminar_cancha'),

    # -------------------------------------------------------
    # RESERVAS (CRUD completo)
    # -------------------------------------------------------
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

    # -------------------------------------------------------
    # USUARIOS (solo admins)
    # -------------------------------------------------------
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]
