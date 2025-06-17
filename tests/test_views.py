"""
Test cases for all views following TDD London School approach.
Target: 100% test coverage for view layer.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.trabajadores.models import Trabajador
from apps.empresa.models import Empresa
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor


class TrabajadorViewTest(TestCase):
    """Test cases for Trabajador views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.trabajador_data = {
            'nombre': 'Ana',
            'apellido': 'Martínez',
            'correo': 'ana.martinez@cosmeticos.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
        self.trabajador = Trabajador.objects.create(**self.trabajador_data)
    
    def test_trabajador_list_view(self):
        """Test trabajador list view displays all workers"""
        url = reverse('trabajadores:list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Martínez')
        self.assertIn('trabajadores', response.context)
    
    def test_trabajador_create_view_get(self):
        """Test trabajador create view GET request"""
        url = reverse('trabajadores:create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_trabajador_create_view_post_valid(self):
        """Test trabajador create view POST with valid data"""
        url = reverse('trabajadores:create')
        new_data = {
            'nombre': 'Carlos',
            'apellido': 'Pérez',
            'correo': 'carlos.perez@cosmeticos.com',
            'cedula': '0987654321',
            'codigo_empleado': 'EMP002'
        }
        
        response = self.client.post(url, data=new_data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Trabajador.objects.filter(cedula='0987654321').exists())
    
    def test_trabajador_create_view_post_invalid(self):
        """Test trabajador create view POST with invalid data"""
        url = reverse('trabajadores:create')
        invalid_data = {
            'nombre': '',  # Missing required field
            'correo': 'invalid-email'  # Invalid email
        }
        
        response = self.client.post(url, data=invalid_data)
        
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertContains(response, 'form')  # Check form is present for re-rendering
    
    def test_trabajador_update_view_get(self):
        """Test trabajador update view GET request"""
        url = reverse('trabajadores:update', kwargs={'pk': self.trabajador.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['object'], self.trabajador)
    
    def test_trabajador_update_view_post_valid(self):
        """Test trabajador update view POST with valid data"""
        url = reverse('trabajadores:update', kwargs={'pk': self.trabajador.pk})
        updated_data = self.trabajador_data.copy()
        updated_data['nombre'] = 'Ana Cristina'
        
        response = self.client.post(url, data=updated_data)
        
        self.assertEqual(response.status_code, 302)
        self.trabajador.refresh_from_db()
        self.assertEqual(self.trabajador.nombre, 'Ana Cristina')
    
    def test_trabajador_delete_view_get(self):
        """Test trabajador delete view GET request"""
        url = reverse('trabajadores:delete', kwargs={'pk': self.trabajador.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.trabajador)
    
    def test_trabajador_delete_view_post(self):
        """Test trabajador delete view POST request"""
        url = reverse('trabajadores:delete', kwargs={'pk': self.trabajador.pk})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Trabajador.objects.filter(pk=self.trabajador.pk).exists())


class EmpresaViewTest(TestCase):
    """Test cases for Empresa views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.empresa_data = {
            'nombre': 'Cosméticos Bella',
            'direccion': 'Calle Principal 123, Quito',
            'mision': 'Proveer productos de belleza de alta calidad',
            'vision': 'Ser la tienda líder en cosméticos del Ecuador',
            'anio_fundacion': 2010,
            'ruc': '1234567890123'
        }
    
    def test_empresa_detail_view_no_empresa(self):
        """Test empresa detail view when no company exists"""
        url = reverse('empresa:detail')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Should show "no info" message according to PRD
    
    def test_empresa_detail_view_with_empresa(self):
        """Test empresa detail view when company exists"""
        empresa = Empresa.objects.create(**self.empresa_data)
        url = reverse('empresa:detail')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cosméticos Bella')
    
    def test_empresa_create_view_get(self):
        """Test empresa create view GET request"""
        url = reverse('empresa:create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_empresa_create_view_post_valid(self):
        """Test empresa create view POST with valid data"""
        url = reverse('empresa:create')
        
        response = self.client.post(url, data=self.empresa_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Empresa.objects.filter(ruc='1234567890123').exists())
    
    def test_empresa_update_view(self):
        """Test empresa update view"""
        empresa = Empresa.objects.create(**self.empresa_data)
        url = reverse('empresa:update')  # No pk needed for singleton
        
        updated_data = self.empresa_data.copy()
        updated_data['nombre'] = 'Cosméticos Premium'
        
        response = self.client.post(url, data=updated_data)
        
        self.assertEqual(response.status_code, 302)
        empresa.refresh_from_db()
        self.assertEqual(empresa.nombre, 'Cosméticos Premium')


class ProductoViewTest(TestCase):
    """Test cases for Producto views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.producto_data = {
            'nombre': 'Lápiz Labial Rojo',
            'descripcion': 'Lápiz labial de larga duración',
            'precio': '25.99',
            'iva': 15
        }
        self.producto = Producto.objects.create(**self.producto_data)
    
    def test_producto_list_view(self):
        """Test producto list view displays all products"""
        url = reverse('productos:list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lápiz Labial Rojo')
        self.assertIn('productos', response.context)
    
    def test_producto_create_view_post_valid(self):
        """Test producto create view POST with valid data"""
        url = reverse('productos:create')
        new_data = {
            'nombre': 'Base de Maquillaje',
            'descripcion': 'Base líquida natural',
            'precio': '35.50',
            'iva': 0
        }
        
        response = self.client.post(url, data=new_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre='Base de Maquillaje').exists())
    
    def test_producto_delete_view(self):
        """Test producto delete view"""
        url = reverse('productos:delete', kwargs={'pk': self.producto.pk})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())


class ProveedorViewTest(TestCase):
    """Test cases for Proveedor views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.proveedor_data = {
            'nombre': 'L\'Oréal Ecuador',
            'descripcion': 'Distribuidor oficial de productos L\'Oréal',
            'telefono': '+593-2-123-4567',
            'pais': 'Ecuador',
            'correo': 'contacto@loreal.ec',
            'direccion': 'Av. Amazonas 456, Quito'
        }
        self.proveedor = Proveedor.objects.create(**self.proveedor_data)
    
    def test_proveedor_list_view(self):
        """Test proveedor list view displays all suppliers"""
        url = reverse('proveedores:list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oréal Ecuador')  # HTML encoding changes the apostrophe
        self.assertIn('proveedores', response.context)
    
    def test_proveedor_create_view_post_valid(self):
        """Test proveedor create view POST with valid data"""
        url = reverse('proveedores:create')
        new_data = {
            'nombre': 'Revlon Internacional',
            'descripcion': 'Proveedor de cosméticos premium',
            'telefono': '+1-555-123-4567',
            'pais': 'Estados Unidos',
            'correo': 'ventas@revlon.com',
            'direccion': '237 Park Avenue, New York'
        }
        
        response = self.client.post(url, data=new_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Proveedor.objects.filter(nombre='Revlon Internacional').exists())


class HomeViewTest(TestCase):
    """Test cases for home and static views"""
    
    def test_home_view(self):
        """Test home page view"""
        url = reverse('home')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # According to PRD, should be static content about cosmetics store


class ViewIntegrationTest(TestCase):
    """Integration tests for view interactions"""
    
    def test_navigation_between_views(self):
        """Test navigation between different section views"""
        # Test that all main views are accessible
        urls_to_test = [
            reverse('home'),
            reverse('trabajadores:list'),
            reverse('productos:list'),
            reverse('proveedores:list'),
            reverse('empresa:detail'),
        ]
        
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed to access {url}")
    
    def test_crud_workflow_integration(self):
        """Test complete CRUD workflow for trabajadores"""
        # Create
        create_url = reverse('trabajadores:create')
        worker_data = {
            'nombre': 'María',
            'apellido': 'González',
            'correo': 'maria.gonzalez@cosmeticos.com',
            'cedula': '1111111111',
            'codigo_empleado': 'EMP999'
        }
        
        response = self.client.post(create_url, data=worker_data)
        self.assertEqual(response.status_code, 302)
        
        # Read (verify creation)
        trabajador = Trabajador.objects.get(cedula='1111111111')
        self.assertEqual(trabajador.nombre, 'María')
        
        # Update
        update_url = reverse('trabajadores:update', kwargs={'pk': trabajador.pk})
        updated_data = worker_data.copy()
        updated_data['nombre'] = 'María José'
        
        response = self.client.post(update_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        
        trabajador.refresh_from_db()
        self.assertEqual(trabajador.nombre, 'María José')
        
        # Delete
        delete_url = reverse('trabajadores:delete', kwargs={'pk': trabajador.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        
        self.assertFalse(Trabajador.objects.filter(pk=trabajador.pk).exists())
    
    def test_form_validation_across_views(self):
        """Test form validation consistency across different views"""
        invalid_data = {
            'nombre': '',
            'correo': 'invalid-email',
            'cedula': 'abc',  # Non-numeric
        }
        
        # Test validation in create view
        create_url = reverse('trabajadores:create')
        response = self.client.post(create_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on form
        
        # Create a valid worker first for update test
        valid_worker = Trabajador.objects.create(
            nombre='Test', apellido='User', correo='test@test.com',
            cedula='9999999999', codigo_empleado='TESTCODE'
        )
        
        # Test validation in update view
        update_url = reverse('trabajadores:update', kwargs={'pk': valid_worker.pk})
        response = self.client.post(update_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on form