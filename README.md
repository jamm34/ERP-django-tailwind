# ERP System (Django + Tailwind)

Sistema ERP desarrollado con Django y Tailwind CSS para la gestion operativa de materiales y proveedores, con control de acceso por roles y permisos.

**Estado:** proyecto en desarrollo para entorno local.

**Autor:** jamm34

**Tabla de contenidos**
1. Vision general
2. Modulos
3. Tecnologias
4. Instalacion rapida
5. Estructura del proyecto
6. Requisitos
7. Pruebas
8. Roadmap
9. Licencia

## Vision general

Este proyecto centraliza procesos internos de una organizacion y ofrece:

- Autenticacion de usuarios con sesiones protegidas.
- Dashboard con accesos por permisos (lectura / lectura-escritura).
- Modulos operativos para Materiales y Proveedores.
- Exportacion e importacion masiva via CSV.
- Interfaz moderna con Tailwind CSS.

## Modulos

### Materiales
- CRUD de materiales.
- Filtros por ID, nombre, tipo y estado.
- Exportacion de listados a CSV.
- Control de permisos (solo lectura / lectura-escritura).

### Proveedores
- CRUD de proveedores.
- Filtros por ID, nombre, pais y estado.
- Exportacion de listados a CSV.
- Carga masiva por CSV con validacion y reporte de errores.
- Descarga de plantilla CSV.

### Usuarios y permisos
- Login/Logout.
- Roles con permisos por modulo (lectura / lectura-escritura).
- Dashboard que muestra accesos segun permisos del usuario.

## Tecnologias

- Python 3.11+
- Django 5.2
- Tailwind CSS (CDN)
- SQLite (entorno local)

## Instalacion rapida

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

## Estructura del proyecto

```
erp/
├── core/              # Dashboard y layout base
├── users/             # Autenticacion y roles
├── materials/         # Modulo de materiales
├── suppliers/         # Modulo de proveedores
├── erp_project/       # Configuracion del proyecto Django
└── manage.py
```

## Requisitos

- Python 3.11 o superior
- pip

## Pruebas

Actualmente no hay pruebas automatizadas. Se recomienda agregar tests unitarios y de integracion en cada app.

## Roadmap

- Incorporar modulos faltantes del ERP (ventas, compras, inventario, contabilidad).
- Anadir API REST para integraciones externas.
- Mejorar la gestion de permisos por rol (UI administrativa).
- Agregar CI/CD y pruebas automatizadas.

## Licencia

Este proyecto no tiene una licencia definida. Si deseas publicarlo o distribuirlo, agrega una licencia en este archivo.
