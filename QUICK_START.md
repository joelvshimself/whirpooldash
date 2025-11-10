# Quick Start - Database Setup

## Error: "Authentication service unavailable"

Si ves este error, necesitas configurar la base de datos primero.

## Pasos Rápidos

### 1. Instalar PostgreSQL (si no lo tienes)

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2. Crear la base de datos

```bash
# Conectar a PostgreSQL
psql postgres

# En el prompt de psql, ejecuta:
CREATE DATABASE whirlpool_dashboard;
\q
```

### 3. Inicializar tablas y usuario admin

```bash
# Asegúrate de estar en el directorio del proyecto
cd /Users/David/Documents/Tec/Semestre\ 7/whirpooldash

# Activa el virtual environment
source venv/bin/activate

# Inicializa las tablas y crea el usuario admin
python scripts/init_db.py
```

Deberías ver:
```
Creating database tables...
Tables created successfully!

Creating admin user...
Admin user created successfully! (username: admin, password: admin)

Database initialization complete!
```

### 4. (Opcional) Poblar con datos dummy

```bash
python scripts/seed_data.py
```

### 5. Configurar el tipo de data source

Crea un archivo `.env` en la raíz del proyecto:

```bash
cat > .env << 'EOF'
DATA_SOURCE_TYPE=database
EOF
```

### 6. Reiniciar la aplicación

```bash
# Detén Streamlit (Ctrl+C)
# Vuelve a iniciar
streamlit run app.py
```

### 7. Login

- Usuario: `admin`
- Contraseña: `admin`

## Troubleshooting

### Error: "could not connect to server"

PostgreSQL no está corriendo:
```bash
brew services start postgresql
```

### Error: "database does not exist"

```bash
createdb whirlpool_dashboard
```

### Error: "relation does not exist"

No has ejecutado init_db.py:
```bash
python scripts/init_db.py
```

## Usar datos mock (sin PostgreSQL)

Si no quieres usar PostgreSQL, puedes usar datos mock:

```bash
# NO crear el archivo .env, o crear con:
echo "DATA_SOURCE_TYPE=mock" > .env

# La app usará datos dummy sin necesidad de DB
streamlit run app.py
```

**NOTA:** Con datos mock, el login NO funcionará porque no hay base de datos para validar usuarios.

