# Aplicación Web Django - Documento de Requerimientos del Producto

## Descripción General del Proyecto
Desarrollar una aplicación web completa para una **tienda de cosméticos** usando el framework Django con integración a base de datos PostgreSQL, implementando el patrón de diseño MVC (Modelo-Vista-Controlador) en Python con operaciones CRUD completas para múltiples entidades de negocio.

## Stack Tecnológico
- **Python**: 3.13
- **Framework**: Django 5.2.2
- **Gestor de Paquetes**: UV (para manejo de dependencias y entornos virtuales)
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML, CSS/Bootstrap, JavaScript (opcional)
- **Adaptador de Base de Datos**: psycopg2

## Configuración de Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'practicatpe2',
        'USER': 'practicausr25',
        'PASSWORD': 'practic35',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Estructura del Proyecto

### Configuración del Proyecto Django
1. Crear proyecto principal de Django
2. Configurar conexión a base de datos PostgreSQL
3. Crear cuatro aplicaciones Django:
   - `trabajadores` (Trabajadores)
   - `empresa` (Empresa)
   - `productos` (Productos)
   - `proveedores` (Proveedores)

### Modelos de Datos

#### Modelo Trabajador
```python
- nombre
- apellido
- correo
- cedula
- codigo_empleado
- imagen
```

#### Modelo Empresa
```python
- nombre
- direccion
- mision
- vision
- anio_fundacion
- ruc
- imagen
```

#### Modelo Producto
```python
- nombre
- descripcion
- precio
- iva (valores: 15 ó 0)
- imagen
```

#### Modelo Proveedor
```python
- nombre
- descripcion
- telefono
- pais
- correo
- direccion
```

## Requerimientos de la Aplicación

### Funcionalidad Principal
1. **Migración de Base de Datos**: Generar y aplicar migraciones para todos los modelos
2. **Operaciones CRUD**: Implementar funcionalidad completa de Crear, Leer, Actualizar, Eliminar para cada aplicación
3. **Vistas y Templates**: Crear vistas correspondientes y plantillas HTML para cada operación CRUD

### Estructura de Páginas y Navegación

**Estructura común en todas las páginas**:
- Título del sitio web + Logo de la tienda de cosméticos (parte superior)
- Menú de navegación estándar
- Contenido específico de cada página con estética apropiada para cosméticos

#### 1. Página Principal (Contenido Estático)
- **Ruta**: `/`
- **Contenido**: Información estática sobre la tienda de cosméticos (NO depende de base de datos)
- **Implementación**: Directamente en HTML (sin datos dinámicos)
- **Estructura**:
  - Título del sitio web + Logo de la tienda de cosméticos
  - Sección "DESCRIPCION DE LA EMPRESA" con carrusel de imágenes (4 imágenes relacionadas con cosméticos)
  - Sección "HISTORIA DE LA EMPRESA" con carrusel de imágenes (4 imágenes sobre la historia de la tienda)
  - Menú de navegación

**IMPORTANTE**: Esta página debe ser completamente estática, codificada directamente en HTML con contenido relacionado a la tienda de cosméticos.

#### 2. Página Nosotros (`/nosotros/`)
- **Lógica de navegación**:
  - **Cuando no existe información de empresa**: 
    - Mostrar "NO SE HA INGRESADO INFORMACION DE LA EMPRESA!!" 
    - Botón "AGREGAR INFORMACION" → redirige a formulario de creación
  - **Cuando existe información de empresa**: 
    - Acceso directo muestra la información de la tienda de cosméticos (nombre, RUC, dirección, misión, visión, año de fundación, imagen)
    - Botón "EDITAR INFORMACION" → redirige a formulario de edición
- **Nota**: Solo una empresa en el sistema (la tienda de cosméticos)

#### 3. Página Trabajadores (`/trabajadores/`)
- **Título de sección**: "NUESTRO PERSONAL"
- **Características**:
  - Mostrar todos los trabajadores de la tienda de cosméticos en formato de tarjetas (2 columnas, 2 filas)
  - Botón "AGREGAR TRABAJADOR" → redirige a formulario de creación
  - Tarjetas individuales mostrando: imagen del colaborador, nombre, correo, tipo de trabajador (ej: consultor de belleza, vendedor, maquillador), código de empleado
  - Botones editar/eliminar funcionales para cada trabajador

#### 4. Página Productos (`/productos/`)
- **Título de sección**: "NUESTROS PRODUCTOS"
- **Características**:
  - Mostrar todos los productos cosméticos en formato de grilla (3 columnas)
  - Botón "AGREGAR PRODUCTO" → redirige a formulario de creación
  - Tarjetas de productos mostrando: imagen del cosmético, nombre del producto, precio, información de IVA (15% o 0%)
  - Botones editar/eliminar funcionales para cada producto
- **Ejemplos de productos**: maquillaje, skincare, fragancias, accesorios de belleza, etc.

#### 5. Página Proveedores (`/proveedores/`)
- **Título de sección**: "NUESTROS PROVEEDORES"
- **Características**:
  - Mostrar todos los proveedores de cosméticos en formato de tarjetas (3 columnas, 2 filas)
  - Botón "AGREGAR PROVEEDOR" → redirige a formulario de creación
  - Tarjetas de proveedores mostrando: nombre, correo, teléfono, país (sin imagen)
  - Botones editar/eliminar funcionales para cada proveedor
- **Ejemplos de proveedores**: marcas de maquillaje, distribuidores de skincare, proveedores de fragancias, etc.

### Funcionalidad de Botones CRUD (Requisito Crítico)

**TODOS los botones deben ser completamente funcionales**:

1. **Botones de Creación**:
   - "AGREGAR TRABAJADOR" → formulario de creación de trabajador
   - "AGREGAR PRODUCTO" → formulario de creación de producto  
   - "AGREGAR PROVEEDOR" → formulario de creación de proveedor
   - "AGREGAR INFORMACION" (empresa) → formulario de creación de empresa

2. **Botones de Edición**:
   - Íconos de editar en cada tarjeta → formularios de edición correspondientes
   - "EDITAR INFORMACION" (empresa) → formulario de edición de empresa

3. **Botones de Eliminación**:
   - Íconos de eliminar en cada tarjeta → confirmación y eliminación del registro

**Todos los formularios deben coincidir exactamente con los campos especificados en cada modelo.**

### Menú de Navegación
Navegación estándar en todas las páginas (según diseños oficiales):
`HOME | NOSOTROS | CLIENTES | PRODUCTOS | TRABAJADORES | PROVEEDORES | SUCURSALES`

**Nota**: CLIENTES y SUCURSALES aparecen en el menú según diseños pero no requieren funcionalidad CRUD.

## Requerimientos de Implementación Técnica

### 1. Configuración de URLs
- Configurar enrutamiento de URLs apropiado para todas las aplicaciones
- **URLs específicas para cada operación CRUD por aplicación**:
  - URLs para trabajadores (listar, crear, editar, eliminar)
  - URLs para empresa (listar, crear, editar, eliminar) 
  - URLs para productos (listar, crear, editar, eliminar)
  - URLs para proveedores (listar, crear, editar, eliminar)
- Implementar patrones de URL RESTful para operaciones CRUD

### 2. Implementación de Vistas
- Vistas basadas en clases o funciones para operaciones CRUD
- **Cada aplicación debe tener sus propias vistas**: trabajadores, empresa, productos, proveedores
- Manejo apropiado de errores y validación
- Manejo de formularios para operaciones de crear/actualizar
- Páginas separadas para formularios de edición/creación

### 3. Templates
- Template base con navegación común
- **Templates individuales para cada operación CRUD de cada aplicación**
- Diseño responsivo usando CSS/Bootstrap
- Funcionalidad de carga y visualización de imágenes

### 4. Archivos Estáticos
- Estilos CSS para diseño responsivo
- JavaScript para UX mejorada (opcional)
- Manejo de archivos multimedia para carga de imágenes

### 5. Formularios
- **Django ModelForms para cada modelo** (Trabajador, Empresa, Producto, Proveedor)
- Validación apropiada y manejo de errores
- Manejo de carga de archivos para imágenes

## Configuración de Dependencias
Usando el gestor de paquetes UV:
```bash
uv add django==5.2.2
uv add psycopg2-binary  # Librería específica requerida para PostgreSQL
uv add Pillow  # para soporte de ImageField
```

**Tecnologías mínimas requeridas**: HTML, CSS o Bootstrap, JavaScript (Opcional), Django, Python, PostgreSQL.

## Configuración de Migración y Base de Datos
1. Crear base de datos PostgreSQL `practicatpe2`
2. Crear usuario de base de datos con credenciales especificadas
3. Ejecutar migraciones de Django para crear tablas: `python manage.py makemigrations` y `python manage.py migrate`
4. Asegurar conectividad apropiada de base de datos
5. **Requisito previo**: Tener instalado el motor de base de datos PostgreSQL

## Criterios de Validación
- Todas las operaciones CRUD deben ser funcionales
- La integración con base de datos debe funcionar correctamente
- Todas las páginas deben renderizar apropiadamente con navegación
- La funcionalidad de carga de imágenes debe funcionar
- Implementación de diseño responsivo
- Manejo apropiado de errores y validación
- Sin sistema de autenticación requerido

## Notas Adicionales
- **Temática del sitio web**: Tienda de cosméticos
- **Paleta de colores sugerida**: Colores apropiados para tienda de cosméticos (tonos rosados, dorados, neutros elegantes, blancos, etc.)
- **Patrón de diseño**: Implementar correctamente el patrón MVC de Django
- **Contenido visual**: Las imágenes y diseño deben reflejar la elegancia y estética propia de una tienda de cosméticos
