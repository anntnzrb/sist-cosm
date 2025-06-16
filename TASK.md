# TASK.md - Cosmetics Store Web Application Development Plan

## Overview
This document outlines the implementation phases for developing a Django-based cosmetics store web application with PostgreSQL database integration, following the MVC pattern and implementing full CRUD operations for multiple business entities.

## Phase 1: Project Setup and Configuration

### 1.1 Environment Setup
- [x] Install Python 3.13
- [x] Install UV package manager
- [x] Create virtual environment using UV
- [x] Install required dependencies:
  - Django 5.2.2
  - psycopg2-binary (PostgreSQL adapter)
  - Pillow (image handling)

### 1.2 Database Setup
- [x] Install PostgreSQL if not already installed
- [x] Create database `practicatpe2`
- [x] Create database user `practicausr25` with password `practic35`
- [x] Grant necessary permissions to the user
- [x] Test database connection

### 1.3 Django Project Initialization
- [x] Create main Django project
- [x] Configure database settings in settings.py
- [x] Configure static and media files settings
- [x] Set up base directory structure

## Phase 2: Django Applications Creation

### 2.1 Create Django Apps
- [x] Create `trabajadores` app (Workers)
- [x] Create `empresa` app (Company)
- [x] Create `productos` app (Products)
- [x] Create `proveedores` app (Suppliers)
- [x] Register all apps in INSTALLED_APPS

### 2.2 URL Configuration
- [x] Configure main project URLs (urls.py)
- [x] Create URL patterns for each app
- [x] Implement RESTful URL patterns for CRUD operations:
  - List view: `/app_name/`
  - Create view: `/app_name/create/`
  - Update view: `/app_name/update/<id>/`
  - Delete view: `/app_name/delete/<id>/`

## Phase 3: Model Implementation

### 3.1 Trabajador (Worker) Model
- [x] Create model with fields:
  - nombre (name)
  - apellido (last name)
  - correo (email)
  - cedula (ID number)
  - codigo_empleado (employee code)
  - imagen (image)
- [x] Add string representation method
- [x] Add model metadata

### 3.2 Empresa (Company) Model
- [x] Create model with fields:
  - nombre (name)
  - direccion (address)
  - mision (mission)
  - vision (vision)
  - anio_fundacion (foundation year)
  - ruc (tax ID)
  - imagen (image)
- [x] Implement singleton pattern (only one company)
- [x] Add string representation method

### 3.3 Producto (Product) Model
- [x] Create model with fields:
  - nombre (name)
  - descripcion (description)
  - precio (price)
  - iva (VAT - choices: 15 or 0)
  - imagen (image)
- [x] Add IVA validation (only 15 or 0)
- [x] Add string representation method

### 3.4 Proveedor (Supplier) Model
- [x] Create model with fields:
  - nombre (name)
  - descripcion (description)
  - telefono (phone)
  - pais (country)
  - correo (email)
  - direccion (address)
- [x] Add string representation method

### 3.5 Database Migrations
- [x] Run makemigrations for all apps
- [x] Apply migrations to database
- [x] Verify database tables creation

## Phase 4: Forms Implementation

### 4.1 Create ModelForms
- [x] TrabajadorForm with all fields and validations
- [x] EmpresaForm with all fields and validations
- [x] ProductoForm with IVA field validation (15 or 0)
- [x] ProveedorForm with all fields and validations

### 4.2 Form Features
- [x] Image upload handling for all forms
- [x] Custom validation methods
- [x] Error message customization
- [x] Bootstrap CSS classes integration

## Phase 5: Views Implementation

### 5.1 Common View Structure
- [x] Create base template context
- [x] Implement error handling decorators
- [x] Create mixins for common functionality

### 5.2 Static Pages
- [x] Home page view (static content)
- [x] Configure static page routing

### 5.3 Trabajadores Views
- [x] List view - display all workers in 2x2 grid
- [x] Create view - add new worker
- [x] Update view - edit worker information
- [x] Delete view - remove worker with confirmation

### 5.4 Empresa Views
- [x] Detail view - display company information
- [x] Create view - add company info (if not exists)
- [x] Update view - edit company information
- [x] Logic for single company instance

### 5.5 Productos Views
- [x] List view - display products in 3-column grid
- [x] Create view - add new product
- [x] Update view - edit product information
- [x] Delete view - remove product with confirmation

### 5.6 Proveedores Views
- [x] List view - display suppliers in 3x2 grid
- [x] Create view - add new supplier
- [x] Update view - edit supplier information
- [x] Delete view - remove supplier with confirmation

## Phase 6: Templates Implementation

### 6.1 Base Templates
- [x] Create base.html with:
  - Site title and cosmetics store logo
  - Navigation menu (HOME | NOSOTROS | CLIENTES | PRODUCTOS | TRABAJADORES | PROVEEDORES | SUCURSALES)
  - Footer section
  - CSS/JS includes
- [x] Configure template inheritance

### 6.2 Home Page Template
- [x] Static HTML content
- [x] Company description section with 4-image carousel
- [x] Company history section with 4-image carousel
- [x] Cosmetics-themed styling

### 6.3 Nosotros (About Us) Templates
- [x] Empty state template (no company info)
- [x] Company detail template
- [x] Edit form template

### 6.4 Trabajadores Templates
- [x] List template - "NUESTRO PERSONAL" title, 2x2 card grid
- [x] Create form template
- [x] Update form template
- [x] Delete confirmation template
- [x] Worker card component (image, name, email, role, employee code)

### 6.5 Productos Templates
- [x] List template - "NUESTROS PRODUCTOS" title, 3-column grid
- [x] Create form template
- [x] Update form template
- [x] Delete confirmation template
- [x] Product card component (image, name, price, IVA info)

### 6.6 Proveedores Templates
- [x] List template - "NUESTROS PROVEEDORES" title, 3x2 grid
- [x] Create form template
- [x] Update form template
- [x] Delete confirmation template
- [x] Supplier card component (name, email, phone, country)

## Phase 7: Static Files and Styling

### 7.1 CSS Implementation
- [x] Create main stylesheet
- [x] Implement cosmetics store color palette (pink, gold, elegant neutrals, white)
- [x] Responsive design using Bootstrap
- [x] Card layouts for each entity type
- [x] Form styling
- [x] Navigation menu styling

### 7.2 JavaScript (Optional)
- [x] Image carousel functionality
- [x] Delete confirmation modals
- [x] Form validation enhancements
- [x] Dynamic UI interactions

### 7.3 Media Files
- [x] Configure media file handling
- [x] Create upload directories for images
- [x] Implement image preview functionality
- [x] Add default/placeholder images

## Phase 8: CRUD Functionality Implementation

### 8.1 Create Operations
- [x] Implement "AGREGAR TRABAJADOR" functionality
- [x] Implement "AGREGAR PRODUCTO" functionality
- [x] Implement "AGREGAR PROVEEDOR" functionality
- [x] Implement "AGREGAR INFORMACION" (company) functionality
- [x] Success message displays
- [x] Redirect to list views after creation

### 8.2 Read Operations
- [x] Display all workers with proper formatting
- [x] Display company information (singleton)
- [x] Display all products with pricing
- [x] Display all suppliers with contact info

### 8.3 Update Operations
- [x] Edit button functionality for all entities
- [x] Pre-populate forms with existing data
- [x] Handle image updates
- [x] Success message displays

### 8.4 Delete Operations
- [x] Delete confirmation dialogs
- [x] Cascade delete handling
- [x] Success message displays
- [x] Redirect after deletion

## Phase 9: Testing and Validation

### 9.1 Model Testing
- [x] Test all model validations
- [x] Test image upload functionality
- [x] Test singleton pattern for Empresa
- [x] Test IVA validation for Producto

### 9.2 Form Testing
- [x] Test form validations
- [x] Test error displays
- [x] Test file upload limits
- [x] Test required field validations

### 9.3 View Testing
- [x] Test all CRUD operations
- [x] Test navigation flow
- [x] Test error handling
- [x] Test redirect logic

### 9.4 Template Testing
- [x] Verify responsive design
- [x] Test on different screen sizes
- [x] Verify all buttons are functional
- [x] Test image display

## Phase 10: Deployment Preparation

### 10.1 Security
- [x] Configure ALLOWED_HOSTS
- [x] Set DEBUG to False for production
- [x] Configure CSRF protection
- [x] Secure media file serving

### 10.2 Performance
- [x] Optimize database queries
- [x] Configure static file serving
- [x] Implement pagination if needed
- [x] Image optimization

### 10.3 Final Checks
- [x] Verify all CRUD operations work
- [x] Check database integrity
- [x] Validate all forms
- [x] Test navigation completeness
- [x] Ensure cosmetics theme consistency

## Critical Requirements Checklist

- [x] All CRUD buttons must be fully functional
- [x] PostgreSQL database integration working
- [x] All pages render correctly with navigation
- [x] Image upload functionality operational
- [x] Responsive design implemented
- [x] Error handling and validation in place
- [x] No authentication system (as per requirements)
- [x] Cosmetics store theme consistent throughout

## Notes
- Menu items "CLIENTES" and "SUCURSALES" appear in navigation but don't require CRUD functionality
- The home page must be completely static (no database dependency)
- Company (Empresa) should only have one instance in the system
- All forms must match exactly the fields specified in each model