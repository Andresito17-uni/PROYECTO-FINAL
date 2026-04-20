from django.urls import path

from . import views

urlpatterns = [
    # Portal de clientes.
    path('', views.portal_inicio, name='portal_inicio'),
    path('canchas/', views.portal_canchas, name='portal_canchas'),
    path('nosotros/', views.portal_nosotros, name='portal_nosotros'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('mi-panel/', views.mi_panel, name='mi_panel'),
    path('reservar/', views.crear_reserva_cliente, name='crear_reserva_cliente'),
    path('reservas/<int:reserva_id>/pagar/', views.pagar_reserva_cliente, name='pagar_reserva_cliente'),
    path('dueno/panel/', views.dueno_panel, name='dueno_panel'),
    path('dueno/canchas/<int:cancha_id>/disponibilidad/', views.actualizar_disponibilidad_cancha, name='actualizar_disponibilidad_cancha'),
    path('dueno/reservas/<int:reserva_id>/estado/', views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    # Zona de gestion (admin interno del negocio).
    path('gestion/', views.gestion_inicio, name='gestion_inicio'),
    path('gestion/usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('gestion/complejos/', views.complejos_lista, name='complejos_lista'),
    path('gestion/complejos/nuevo/', views.crear_complejo, name='crear_complejo'),
    path('gestion/canchas/', views.canchas_lista, name='canchas_lista'),
    path('gestion/canchas/nueva/', views.crear_cancha, name='crear_cancha'),
    path('gestion/tipos-cancha/nuevo/', views.crear_tipo_cancha, name='crear_tipo_cancha'),
    path('gestion/reservas/', views.reservas_lista, name='reservas_lista'),
    path('gestion/pagos/', views.pagos_lista, name='pagos_lista'),
    path('gestion/reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('gestion/pagos/nuevo/', views.crear_pago, name='crear_pago'),
    path('gestion/catalogos/', views.catalogos_lista, name='catalogos_lista'),
]
