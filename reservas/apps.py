# ============================================================
# CONFIGURACIÓN DE LA APP - reservas/apps.py
# Este archivo le dice a Django cómo se llama nuestra app.
# ============================================================
from django.apps import AppConfig

class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas'
    verbose_name = 'Sistema de Reservas'  # Nombre que aparece en el panel admin
