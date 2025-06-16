# Cosmetics Store - Django Web Application

A Django-based cosmetics store web application with full CRUD operations for workers, company information, products, and suppliers.

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Start the application
docker-compose up --build

# Access the app
http://localhost:8000
```

### Option 2: Local Development
```bash
# Install dependencies
uv sync

# Setup PostgreSQL database
sudo -u postgres psql
CREATE DATABASE practicatpe2;
CREATE USER practicausr25 WITH PASSWORD 'practic35';
GRANT ALL PRIVILEGES ON DATABASE practicatpe2 TO practicausr25;
\q

# Run migrations and start server
uv run python manage.py migrate --settings=cosmeticos_store.settings_local
uv run python manage.py runserver --settings=cosmeticos_store.settings_local
```

## Access Points
- **Homepage**: http://localhost:8000/
- **Company Info**: http://localhost:8000/nosotros/
- **Workers**: http://localhost:8000/trabajadores/
- **Products**: http://localhost:8000/productos/
- **Suppliers**: http://localhost:8000/proveedores/

## Database Credentials
- **Database**: `practicatpe2`
- **User**: `practicausr25`
- **Password**: `practic35`

## Technology Stack
- Django 5.2.2 + PostgreSQL + Bootstrap