# ============================================================
# CONFIGURACIÓN DEL PROYECTO DJANGO - config/settings.py
# Este archivo controla TODA la configuración del proyecto:
# base de datos, aplicaciones instaladas, archivos estáticos, etc.
# ============================================================

from pathlib import Path

# BASE_DIR = la carpeta raíz del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ CLAVE SECRETA: En producción real NUNCA la dejes aquí.
# Usa variables de entorno (python-decouple o dotenv).
SECRET_KEY = 'django-insecure-canchas-deportivas-2024-cambiar-en-produccion'

# DEBUG=True muestra errores detallados. En producción debe ser False.
DEBUG = True

# Hosts permitidos. En producción agrega tu dominio real.
ALLOWED_HOSTS = ['*']


# -------------------------------------------------------
# APLICACIONES INSTALADAS
# Aquí declaras todas las apps que usa el proyecto.
# -------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',       # Panel de administración automático
    'django.contrib.auth',        # Sistema de autenticación
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # Manejo de sesiones (login/logout)
    'django.contrib.messages',    # Mensajes flash (éxito, error, etc.)
    'django.contrib.staticfiles', # Archivos CSS, JS, imágenes
    'reservas',                   # ← Nuestra app principal
]

# Middleware: capas que procesan cada request/response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección anti-CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'  # Archivo donde están las URLs principales

# Configuración de los templates (archivos HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django buscará templates en la carpeta "templates" dentro de cada app
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# -------------------------------------------------------
# BASE DE DATOS
# Por defecto usamos SQLite (un archivo .db local).
# Para producción cambia a PostgreSQL o MySQL.
# -------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Archivo de la base de datos
    }
}

# Validaciones de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------
# MODELO DE USUARIO PERSONALIZADO
# Le decimos a Django que use nuestro modelo Usuario
# en lugar del modelo de usuario por defecto.
# -------------------------------------------------------
AUTH_USER_MODEL = 'reservas.Usuario'

# Idioma y zona horaria
LANGUAGE_CODE = 'es-co'  # Español Colombia
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------
# ARCHIVOS ESTÁTICOS (CSS, JS, imágenes)
# Se sirven desde la carpeta "static/"
# -------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Archivos subidos por usuarios (fotos de perfil, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------
# REDIRECCIONES DE LOGIN
# Después de hacer login, redirige al dashboard.
# Después de logout, redirige al login.
# -------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
