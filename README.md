# ERP System (Django + Tailwind)

Sistema ERP desarrollado con **Django** y **Tailwind CSS** orientado a la gestión operativa de módulos clave como materiales y proveedores, con control de acceso por roles y permisos.

## 🧭 Visión general

Este proyecto centraliza procesos internos de una organización, proporcionando:

- Autenticación de usuarios con sesiones protegidas.
- Dashboard con accesos por permisos (lectura/escritura).
- Módulos operativos para **Materiales** y **Proveedores**.
- Exportación e importación masiva vía **CSV**.
- Interfaz moderna con **Tailwind CSS**.

## 🧩 Módulos disponibles

### ✅ Materiales
- CRUD de materiales.
- Filtros por ID, nombre, tipo y estado.
- Exportación de listados a CSV.
- Control de permisos (solo lectura / lectura-escritura).

### ✅ Proveedores
- CRUD de proveedores.
- Filtros por ID, nombre, país y estado.
- Exportación de listados a CSV.
- Carga masiva por CSV con validación y reporte de errores.
- Descarga de plantilla CSV.

### 🔐 Usuarios y Permisos
- Login/Logout.
- Roles con permisos por módulo (lectura / lectura-escritura).
- Dashboard que muestra accesos según permisos del usuario.

## 🛠️ Tecnologías

- **Python 3.11+**
- **Django 5.2**
- **Tailwind CSS** (CDN)
- **SQLite** (entorno local)

## ⚙️ Instalación rápida

```bash
# 1) Crear entorno virtual
python -m venv env

# 2) Activar entorno (Windows)
env\Scripts\activate

# 3) Instalar dependencias
pip install -r requirements.txt

# 4) Migraciones
python manage.py migrate

# 5) Crear superusuario (opcional)
python manage.py createsuperuser

# 6) Ejecutar servidor
python manage.py runserver
```

Acceso local: `http://127.0.0.1:8000/`

## 📂 Estructura del proyecto

```
erp/
├── core/              # Dashboard y layout base
├── users/             # Autenticación y roles
├── materials/         # Módulo de materiales
├── suppliers/         # Módulo de proveedores
├── erp_project/       # Configuración del proyecto Django
└── manage.py
```

## ✅ Requisitos

- Python 3.11 o superior
- pip

## 🧪 Pruebas

Actualmente no hay pruebas automatizadas. Se recomienda agregar tests unitarios y de integración en cada app.

## 🚀 Próximos pasos sugeridos

- Incorporar módulos faltantes del ERP (ventas, compras, inventario, contabilidad).
- Añadir API REST para integraciones externas.
- Mejorar la gestión de permisos por rol (UI administrativa).
- Agregar CI/CD y pruebas automatizadas.

## 📄 Licencia

Este proyecto no tiene una licencia definida. Si deseas publicarlo o distribuirlo, agrega una licencia en este archivo.

---

**Autor:** jamm34