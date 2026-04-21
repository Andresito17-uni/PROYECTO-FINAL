from django.contrib import admin
from django.urls import path
from principal.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home), # Esto hace que al entrar a la página se vea tu HTML
]