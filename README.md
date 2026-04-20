# Sistema Web de Reservas (Django)

Proyecto base en Django para gestionar:
- usuarios y roles
- complejos y canchas
- reservas
- pagos y sus estados

## 1) Crear y activar entorno virtual

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Instalar dependencias
```powershell
pip install -r requirements.txt
```

## 3) Ejecutar migraciones (crear tablas)
```powershell
python manage.py makemigrations
python manage.py migrate
```

## 4) Crear superusuario para panel admin
```powershell
python manage.py createsuperuser
```

## 5) Levantar servidor
```powershell
python manage.py runserver
```

Luego abre:
- Aplicacion: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Credenciales demo (login del portal)

Contrasena para todos: `123456`

- Administrador: `admin@reservarr.com`
- Cliente: `carlos@correo.com`
- Cliente: `maria@correo.com`
- Dueno de complejo: `dueno@complejo.com`

## Como esta organizado el proyecto

- `config/settings.py`: configuracion general del proyecto (apps, idioma, zona horaria, estaticos).
- `core/models.py`: tablas de tu base de datos representadas en clases Django.
- `core/forms.py`: formularios para crear reservas y pagos.
- `core/views.py`: logica para mostrar listas, dashboard y guardar formularios.
- `core/urls.py`: rutas de la app.
- `templates/`: parte visual (HTML).
- `static/css/styles.css`: estilos personalizados.

## Notas para aprender rapido

1. En Django, cada modelo equivale a una tabla.
2. Cada `ForeignKey` equivale a una relacion entre tablas.
3. Las vistas toman datos de modelos y los envian a templates.
4. Los templates muestran los datos en HTML.
5. Los formularios validan entradas antes de guardar.
