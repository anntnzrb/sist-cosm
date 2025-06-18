# Tienda de Cosméticos

Django app con CRUD para tienda de cosméticos.

## Ejecutar

### Con Docker
```bash
git clone <url>
cd sist-cosm
docker-compose up --build
```

### Sin Docker
```bash
git clone <url>
cd sist-cosm
pip install uv && uv sync

# Configurar PostgreSQL
sudo -u postgres psql
CREATE DATABASE practicatpe2;
CREATE USER practicausr25 WITH PASSWORD 'practic35';
\q

# Ejecutar
uv run python manage.py migrate
uv run python manage.py runserver
```

**Ver**: http://localhost:8000

## Producción

Para configuración de producción:
```bash
docker compose run --rm -e DJANGO_SETTINGS_MODULE=cosmeticos_store.settings_production web uv run python manage.py runserver
```

**Especificaciones**: [docs/prd.md](docs/prd.md)