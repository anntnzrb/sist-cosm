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
- [ ] Install PostgreSQL if not already installed
- [ ] Create database `practicatpe2`
- [ ] Create database user `practicausr25` with password `practic35`
- [ ] Grant necessary permissions to the user
- [ ] Test database connection

### 1.3 Django Project Initialization
- [ ] Create main Django project
- [ ] Configure database settings in settings.py
- [ ] Configure static and media files settings
- [ ] Set up base directory structure

## Phase 2: Django Applications Creation

### 2.1 Create Django Apps
- [ ] Create `trabajadores` app (Workers)
- [ ] Create `empresa` app (Company)
- [ ] Create `productos` app (Products)
- [ ] Create `proveedores` app (Suppliers)
- [ ] Register all apps in INSTALLED_APPS

### 2.2 URL Configuration
- [ ] Configure main project URLs (urls.py)
- [ ] Create URL patterns for each app
- [ ] Implement RESTful URL patterns for CRUD operations:
  - List view: `/app_name/`
  - Create view: `/app_name/create/`
  - Update view: `/app_name/update/<id>/`
  - Delete view: `/app_name/delete/<id>/`

## Phase 3: Model Implementation

### 3.1 Trabajador (Worker) Model
- [ ] Create model with fields:
  - nombre (name)
  - apellido (last name)
  - correo (email)
  - cedula (ID number)
  - codigo_empleado (employee code)
  - imagen (image)
- [ ] Add string representation method
- [ ] Add model metadata

### 3.2 Empresa (Company) Model
- [ ] Create model with fields:
  - nombre (name)
  - direccion (address)
  - mision (mission)
  - vision (vision)
  - anio_fundacion (foundation year)
  - ruc (tax ID)
  - imagen (image)
- [ ] Implement singleton pattern (only one company)
- [ ] Add string representation method

### 3.3 Producto (Product) Model
- [ ] Create model with fields:
  - nombre (name)
  - descripcion (description)
  - precio (price)
  - iva (VAT - choices: 15 or 0)
  - imagen (image)
- [ ] Add IVA validation (only 15 or 0)
- [ ] Add string representation method

### 3.4 Proveedor (Supplier) Model
- [ ] Create model with fields:
  - nombre (name)
  - descripcion (description)
  - telefono (phone)
  - pais (country)
  - correo (email)
  - direccion (address)
- [ ] Add string representation method

### 3.5 Database Migrations
- [ ] Run makemigrations for all apps
- [ ] Apply migrations to database
- [ ] Verify database tables creation

## Phase 4: Forms Implementation

### 4.1 Create ModelForms
- [ ] TrabajadorForm with all fields and validations
- [ ] EmpresaForm with all fields and validations
- [ ] ProductoForm with IVA field validation (15 or 0)
- [ ] ProveedorForm with all fields and validations

### 4.2 Form Features
- [ ] Image upload handling for all forms
- [ ] Custom validation methods
- [ ] Error message customization
- [ ] Bootstrap CSS classes integration

## Phase 5: Views Implementation

### 5.1 Common View Structure
- [ ] Create base template context
- [ ] Implement error handling decorators
- [ ] Create mixins for common functionality

### 5.2 Static Pages
- [ ] Home page view (static content)
- [ ] Configure static page routing

### 5.3 Trabajadores Views
- [ ] List view - display all workers in 2x2 grid
- [ ] Create view - add new worker
- [ ] Update view - edit worker information
- [ ] Delete view - remove worker with confirmation

### 5.4 Empresa Views
- [ ] Detail view - display company information
- [ ] Create view - add company info (if not exists)
- [ ] Update view - edit company information
- [ ] Logic for single company instance

### 5.5 Productos Views
- [ ] List view - display products in 3-column grid
- [ ] Create view - add new product
- [ ] Update view - edit product information
- [ ] Delete view - remove product with confirmation

### 5.6 Proveedores Views
- [ ] List view - display suppliers in 3x2 grid
- [ ] Create view - add new supplier
- [ ] Update view - edit supplier information
- [ ] Delete view - remove supplier with confirmation

## Phase 6: Templates Implementation

### 6.1 Base Templates
- [ ] Create base.html with:
  - Site title and cosmetics store logo
  - Navigation menu (HOME | NOSOTROS | CLIENTES | PRODUCTOS | TRABAJADORES | PROVEEDORES | SUCURSALES)
  - Footer section
  - CSS/JS includes
- [ ] Configure template inheritance

### 6.2 Home Page Template
- [ ] Static HTML content
- [ ] Company description section with 4-image carousel
- [ ] Company history section with 4-image carousel
- [ ] Cosmetics-themed styling

### 6.3 Nosotros (About Us) Templates
- [ ] Empty state template (no company info)
- [ ] Company detail template
- [ ] Edit form template

### 6.4 Trabajadores Templates
- [ ] List template - "NUESTRO PERSONAL" title, 2x2 card grid
- [ ] Create form template
- [ ] Update form template
- [ ] Delete confirmation template
- [ ] Worker card component (image, name, email, role, employee code)

### 6.5 Productos Templates
- [ ] List template - "NUESTROS PRODUCTOS" title, 3-column grid
- [ ] Create form template
- [ ] Update form template
- [ ] Delete confirmation template
- [ ] Product card component (image, name, price, IVA info)

### 6.6 Proveedores Templates
- [ ] List template - "NUESTROS PROVEEDORES" title, 3x2 grid
- [ ] Create form template
- [ ] Update form template
- [ ] Delete confirmation template
- [ ] Supplier card component (name, email, phone, country)

## Phase 7: Static Files and Styling

### 7.1 CSS Implementation
- [ ] Create main stylesheet
- [ ] Implement cosmetics store color palette (pink, gold, elegant neutrals, white)
- [ ] Responsive design using Bootstrap
- [ ] Card layouts for each entity type
- [ ] Form styling
- [ ] Navigation menu styling

### 7.2 JavaScript (Optional)
- [ ] Image carousel functionality
- [ ] Delete confirmation modals
- [ ] Form validation enhancements
- [ ] Dynamic UI interactions

### 7.3 Media Files
- [ ] Configure media file handling
- [ ] Create upload directories for images
- [ ] Implement image preview functionality
- [ ] Add default/placeholder images

## Phase 8: CRUD Functionality Implementation

### 8.1 Create Operations
- [ ] Implement "AGREGAR TRABAJADOR" functionality
- [ ] Implement "AGREGAR PRODUCTO" functionality
- [ ] Implement "AGREGAR PROVEEDOR" functionality
- [ ] Implement "AGREGAR INFORMACION" (company) functionality
- [ ] Success message displays
- [ ] Redirect to list views after creation

### 8.2 Read Operations
- [ ] Display all workers with proper formatting
- [ ] Display company information (singleton)
- [ ] Display all products with pricing
- [ ] Display all suppliers with contact info

### 8.3 Update Operations
- [ ] Edit button functionality for all entities
- [ ] Pre-populate forms with existing data
- [ ] Handle image updates
- [ ] Success message displays

### 8.4 Delete Operations
- [ ] Delete confirmation dialogs
- [ ] Cascade delete handling
- [ ] Success message displays
- [ ] Redirect after deletion

## Phase 9: Testing and Validation

### 9.1 Model Testing
- [ ] Test all model validations
- [ ] Test image upload functionality
- [ ] Test singleton pattern for Empresa
- [ ] Test IVA validation for Producto

### 9.2 Form Testing
- [ ] Test form validations
- [ ] Test error displays
- [ ] Test file upload limits
- [ ] Test required field validations

### 9.3 View Testing
- [ ] Test all CRUD operations
- [ ] Test navigation flow
- [ ] Test error handling
- [ ] Test redirect logic

### 9.4 Template Testing
- [ ] Verify responsive design
- [ ] Test on different screen sizes
- [ ] Verify all buttons are functional
- [ ] Test image display

## Phase 10: Deployment Preparation

### 10.1 Security
- [ ] Configure ALLOWED_HOSTS
- [ ] Set DEBUG to False for production
- [ ] Configure CSRF protection
- [ ] Secure media file serving

### 10.2 Performance
- [ ] Optimize database queries
- [ ] Configure static file serving
- [ ] Implement pagination if needed
- [ ] Image optimization

### 10.3 Final Checks
- [ ] Verify all CRUD operations work
- [ ] Check database integrity
- [ ] Validate all forms
- [ ] Test navigation completeness
- [ ] Ensure cosmetics theme consistency

## Critical Requirements Checklist

- [ ] All CRUD buttons must be fully functional
- [ ] PostgreSQL database integration working
- [ ] All pages render correctly with navigation
- [ ] Image upload functionality operational
- [ ] Responsive design implemented
- [ ] Error handling and validation in place
- [ ] No authentication system (as per requirements)
- [ ] Cosmetics store theme consistent throughout

## Notes
- Menu items "CLIENTES" and "SUCURSALES" appear in navigation but don't require CRUD functionality
- The home page must be completely static (no database dependency)
- Company (Empresa) should only have one instance in the system
- All forms must match exactly the fields specified in each model