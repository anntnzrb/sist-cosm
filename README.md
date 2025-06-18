# Tienda de Cosméticos

Django app con CRUD para tienda de cosméticos.

## Ejecutar

### Con Docker
```bash
docker-compose up --build
```

### Sin Docker
```bash
uv sync

# PostgreSQL
sudo -u postgres psql
CREATE DATABASE practicatpe2;
CREATE USER practicausr25 WITH PASSWORD 'practic35';
GRANT ALL PRIVILEGES ON DATABASE practicatpe2 TO practicausr25;
\q

# Ejecutar (usar settings_local.py para localhost)
uv run python manage.py migrate --settings=cosmeticos_store.settings_local
uv run python manage.py createsuperuser --settings=cosmeticos_store.settings_local
uv run python manage.py runserver --settings=cosmeticos_store.settings_local
```

**Ver**: http://localhost:8000

## Producción

Para configuración de producción:
```bash
docker compose run --rm -e DJANGO_SETTINGS_MODULE=cosmeticos_store.settings_production web uv run python manage.py runserver
```

**Especificaciones**: [docs/prd.md](docs/prd.md)
