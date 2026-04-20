# ============================================================
# URLs PRINCIPALES DEL PROYECTO - config/urls.py
# Este archivo es el "mapa" de la aplicación.
# Cada URL se conecta con una vista (función en views.py).
# ============================================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración automático de Django
    # Entra en: http://localhost:8000/admin/
    path('admin/', admin.site.urls),

    # Todas las URLs de nuestra app "reservas"
    # El prefijo '' significa que van en la raíz del sitio
    path('', include('reservas.urls')),
]

# En modo DEBUG, Django sirve los archivos de media (imágenes subidas)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
