# ⚽ SportField — Sistema de Reservas de Canchas Deportivas
### Desarrollado con Django (Python) | Diseño Premium Dark

---

## 📋 ¿Qué hace esta aplicación?

SportField es un sistema web completo para gestionar reservas de canchas deportivas.
Incluye: usuarios, roles, complejos, canchas, reservas y pagos.

---

## 🚀 CÓMO EJECUTAR EL PROYECTO (paso a paso)

### 1. Instalar Python y pip
Descarga Python desde: https://www.python.org/downloads/
(Asegúrate de marcar "Add Python to PATH" al instalar)

### 2. Instalar Django
Abre la terminal (CMD o PowerShell) en la carpeta del proyecto:
```
pip install django
```

### 3. Crear las tablas en la base de datos
```
python manage.py makemigrations
python manage.py migrate
```
Esto crea el archivo db.sqlite3 con todas las tablas.

### 4. Llenar con datos de prueba
```
python poblar_datos.py
```
Esto crea usuarios, complejos y canchas de ejemplo.

### 5. ¡Ejecutar el servidor!
```
python manage.py runserver
```
Luego abre tu navegador en: **http://127.0.0.1:8000/**

---

## 👤 Usuarios de prueba

| Usuario | Contraseña | Rol           |
|---------|------------|---------------|
| admin   | admin123   | Administrador |
| juan    | juan1234   | Cliente       |

---

## 📁 Estructura del proyecto

```
canchas_project/
│
├── config/               ← Configuración principal de Django
│   ├── settings.py       ← Configuración (base de datos, apps, etc.)
│   └── urls.py           ← URLs raíz del proyecto
│
├── reservas/             ← App principal
│   ├── models.py         ← Tablas de la base de datos
│   ├── views.py          ← Lógica del servidor (Python)
│   ├── forms.py          ← Formularios con validación
│   ├── urls.py           ← URLs de la app
│   └── admin.py          ← Panel de administración
│
├── templates/            ← Archivos HTML
│   ├── base.html         ← Esqueleto base con navbar
│   ├── dashboard.html    ← Panel principal
│   ├── auth/             ← Login y Registro
│   ├── complejos/        ← CRUD de complejos
│   ├── canchas/          ← CRUD de canchas
│   ├── reservas/         ← CRUD de reservas
│   └── usuarios/         ← Lista de usuarios
│
├── static/
│   ├── css/estilos.css   ← Todo el diseño visual
│   └── js/app.js         ← Interactividad JavaScript
│
├── poblar_datos.py       ← Script de datos de prueba
├── manage.py             ← Comandos de Django
└── db.sqlite3            ← Base de datos (se crea al migrar)
```

---

## 🗄️ Modelos (tablas de la base de datos)

| Modelo        | Descripción                                    |
|---------------|------------------------------------------------|
| Usuario       | Usuarios del sistema (extiende Django Auth)    |
| Rol           | Administrador, Cliente, etc.                   |
| UsuarioRol    | Relación muchos-a-muchos Usuario ↔ Rol         |
| Complejo      | Lugar físico con múltiples canchas             |
| TipoCancha    | Fútbol, Baloncesto, Tenis, etc.                |
| Cancha        | Cancha específica dentro de un complejo        |
| EstadoReserva | Pendiente, Confirmada, Cancelada, Completada   |
| MetodoPago    | Efectivo, Tarjeta, Transferencia, Nequi        |
| EstadoPago    | Pendiente, Pagado, Rechazado, Reembolsado      |
| Pago          | Registro de pago de una reserva                |
| Reserva       | Reserva de cancha (usuario + cancha + horario) |

---

## 🎨 Diseño
- **Tema**: Dark premium con acento verde neón
- **Tipografía**: Syne (títulos) + DM Sans (cuerpo)
- **Totalmente responsive** para móvil, tablet y desktop

---

## 🔧 Panel de Administración
Django incluye un panel de admin automático en:
**http://127.0.0.1:8000/admin/**
Inicia sesión con: `admin / admin123`
