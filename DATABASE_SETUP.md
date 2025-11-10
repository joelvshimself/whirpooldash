# Database Setup Guide

Este documento explica cómo configurar y usar la base de datos PostgreSQL con Whirlpool Dashboard.

## Prerequisitos

1. PostgreSQL instalado y corriendo
2. Base de datos creada (por defecto: `whirlpool_dashboard`)
3. Usuario de PostgreSQL con permisos (por defecto: `postgres`)

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- SQLAlchemy (ORM)
- psycopg2-binary (PostgreSQL driver)
- alembic (Migrations, opcional)

## Configuración

### Variables de Entorno

Puedes configurar la conexión a la base de datos mediante variables de entorno o usando los valores por defecto en `config.py`:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=whirlpool_dashboard
export DB_USER=postgres
export DB_PASSWORD=postgres
```

O usar la URL completa:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/whirlpool_dashboard
```

### Cambiar Fuente de Datos

En `config.py` o mediante variable de entorno:

```bash
# Para usar datos mock (por defecto)
export DATA_SOURCE_TYPE=mock

# Para usar PostgreSQL
export DATA_SOURCE_TYPE=database
```

## Inicialización de la Base de Datos

### Paso 1: Crear Base de Datos

Desde psql o tu cliente de PostgreSQL favorito:

```sql
CREATE DATABASE whirlpool_dashboard;
```

### Paso 2: Inicializar Tablas y Usuario Admin

```bash
python scripts/init_db.py
```

Este script:
- Crea todas las tablas necesarias (users, price_history, kpis, skus)
- Crea el usuario admin (username: `admin`, password: `admin`)

### Paso 3: Poblar con Datos Dummy

```bash
python scripts/seed_data.py
```

Este script inserta:
- 200 registros de historial de precios
- 30 días de KPIs
- 10 registros de SKUs

## Uso

### 1. Iniciar la Aplicación con Base de Datos

```bash
# Configurar para usar base de datos
export DATA_SOURCE_TYPE=database

# Iniciar Streamlit
streamlit run app.py
```

### 2. Login

- Usuario: `admin`
- Contraseña: `admin`

## Estructura de la Base de Datos

### Tabla: users
- `id`: Integer (PK)
- `username`: String(50) UNIQUE
- `password_hash`: String(255)
- `created_at`: DateTime

### Tabla: price_history
- `id`: Integer (PK)
- `sku`: String(50)
- `region`: String(100)
- `partner`: String(100)
- `release_date`: DateTime
- `price`: Float
- `created_at`: DateTime

### Tabla: kpis
- `id`: Integer (PK)
- `date`: Date UNIQUE
- `todays_money`: Float
- `todays_users`: Integer
- `money_change`: Float
- `users_change`: Float
- `created_at`: DateTime

### Tabla: skus
- `id`: Integer (PK)
- `company`: String(255)
- `icon`: String(10)
- `members`: Integer
- `budget`: Float (nullable)
- `completion`: Integer
- `created_at`: DateTime

## Arquitectura

```
app.py (Streamlit)
    ↓
services/data_service.py (Singleton)
    ↓
data/database_data_source.py (Implementa DataSource)
    ↓
data/models.py (SQLAlchemy Models)
    ↓
PostgreSQL
```

## Autenticación

- Implementación dummy para desarrollo
- Passwords hasheados con SHA256
- Endpoint: `POST /api/auth/login`
- Session state en Streamlit

## Tips

1. **Resetear la base de datos:**
   ```bash
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

2. **Volver a datos mock:**
   ```bash
   export DATA_SOURCE_TYPE=mock
   ```

3. **Conexión manual a PostgreSQL:**
   ```bash
   psql -U postgres -d whirlpool_dashboard
   ```

4. **Ver logs de SQLAlchemy:**
   En `data/models.py`, cambiar `echo=False` a `echo=True` en `create_engine()`

## Troubleshooting

### Error: "could not connect to server"
- Verifica que PostgreSQL esté corriendo
- Verifica host y puerto en config.py

### Error: "relation does not exist"
- Ejecuta `python scripts/init_db.py`

### Error: "FATAL: database does not exist"
- Crea la base de datos: `CREATE DATABASE whirlpool_dashboard;`

### Login no funciona
- Verifica que init_db.py se haya ejecutado correctamente
- Verifica que el backend FastAPI esté corriendo

