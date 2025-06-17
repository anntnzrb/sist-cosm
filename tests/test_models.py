"""
Test cases for all models following TDD London School approach.
Target: 100% test coverage for model layer.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.trabajadores.models import Trabajador
from apps.empresa.models import Empresa
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor


class TrabajadorModelTest(TestCase):
    """Test cases for Trabajador model"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'nombre': 'Ana',
            'apellido': 'García',
            'correo': 'ana.garcia@cosmeticos.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_trabajador_creation_with_valid_data(self):
        """Test creating a worker with valid data"""
        trabajador = Trabajador.objects.create(**self.valid_data)
        self.assertEqual(trabajador.nombre, 'Ana')
        self.assertEqual(trabajador.apellido, 'García')
        self.assertEqual(trabajador.correo, 'ana.garcia@cosmeticos.com')
        self.assertEqual(trabajador.cedula, '1234567890')
        self.assertEqual(trabajador.codigo_empleado, 'EMP001')
    
    def test_trabajador_string_representation(self):
        """Test the string representation of worker"""
        trabajador = Trabajador.objects.create(**self.valid_data)
        self.assertEqual(str(trabajador), 'Ana García')
    
    def test_trabajador_unique_cedula_constraint(self):
        """Test that cedula must be unique"""
        Trabajador.objects.create(**self.valid_data)
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['correo'] = 'otro@email.com'
        duplicate_data['codigo_empleado'] = 'EMP002'
        
        with self.assertRaises(IntegrityError):
            Trabajador.objects.create(**duplicate_data)
    
    def test_trabajador_unique_codigo_empleado_constraint(self):
        """Test that codigo_empleado must be unique"""
        Trabajador.objects.create(**self.valid_data)
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['correo'] = 'otro@email.com'
        duplicate_data['cedula'] = '0987654321'
        
        with self.assertRaises(IntegrityError):
            Trabajador.objects.create(**duplicate_data)
    
    def test_trabajador_ordering(self):
        """Test default ordering by nombre, apellido"""
        Trabajador.objects.create(
            nombre='Zara', apellido='Alvarez', correo='zara@test.com',
            cedula='111', codigo_empleado='EMP001'
        )
        Trabajador.objects.create(
            nombre='Ana', apellido='Benítez', correo='ana@test.com',
            cedula='222', codigo_empleado='EMP002'
        )
        
        trabajadores = list(Trabajador.objects.all())
        self.assertEqual(trabajadores[0].nombre, 'Ana')
        self.assertEqual(trabajadores[1].nombre, 'Zara')


class EmpresaModelTest(TestCase):
    """Test cases for Empresa model (singleton pattern)"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'nombre': 'Cosméticos Bella',
            'direccion': 'Calle Principal 123, Quito',
            'mision': 'Proveer productos de belleza de alta calidad',
            'vision': 'Ser la tienda líder en cosméticos del Ecuador',
            'anio_fundacion': 2010,
            'ruc': '1234567890123'
        }
    
    def test_empresa_creation_with_valid_data(self):
        """Test creating company with valid data"""
        empresa = Empresa.objects.create(**self.valid_data)
        self.assertEqual(empresa.nombre, 'Cosméticos Bella')
        self.assertEqual(empresa.direccion, 'Calle Principal 123, Quito')
        self.assertEqual(empresa.anio_fundacion, 2010)
        self.assertEqual(empresa.ruc, '1234567890123')
    
    def test_empresa_string_representation(self):
        """Test the string representation of company"""
        empresa = Empresa.objects.create(**self.valid_data)
        self.assertEqual(str(empresa), 'Cosméticos Bella')
    
    def test_empresa_singleton_constraint(self):
        """Test that only one company can exist (singleton pattern)"""
        Empresa.objects.create(**self.valid_data)
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['nombre'] = 'Otra Empresa'
        duplicate_data['ruc'] = 'different_ruc'
        
        with self.assertRaises(ValidationError):
            Empresa.objects.create(**duplicate_data)


class ProductoModelTest(TestCase):
    """Test cases for Producto model"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'nombre': 'Lápiz Labial Rojo Clásico',
            'descripcion': 'Lápiz labial de larga duración con color intenso',
            'precio': 25.99,
            'iva': 15
        }
    
    def test_producto_creation_with_valid_data(self):
        """Test creating product with valid data"""
        producto = Producto.objects.create(**self.valid_data)
        self.assertEqual(producto.nombre, 'Lápiz Labial Rojo Clásico')
        self.assertEqual(producto.precio, 25.99)
        self.assertEqual(producto.iva, 15)
    
    def test_producto_string_representation(self):
        """Test the string representation of product"""
        producto = Producto.objects.create(**self.valid_data)
        self.assertEqual(str(producto), 'Lápiz Labial Rojo Clásico')
    
    def test_producto_iva_choices(self):
        """Test IVA can only be 0 or 15"""
        # Test valid IVA values
        producto_0 = Producto.objects.create(**{**self.valid_data, 'iva': 0, 'nombre': 'Producto sin IVA'})
        self.assertEqual(producto_0.iva, 0)
        
        producto_15 = Producto.objects.create(**{**self.valid_data, 'iva': 15, 'nombre': 'Producto con IVA'})
        self.assertEqual(producto_15.iva, 15)
    
    def test_producto_precio_calculation(self):
        """Test price calculation method with IVA"""
        producto = Producto.objects.create(**self.valid_data)
        expected_price = 25.99 * 1.15  # 25.99 + 15% IVA
        self.assertAlmostEqual(producto.get_precio_con_iva(), expected_price, places=2)


class ProveedorModelTest(TestCase):
    """Test cases for Proveedor model"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'nombre': 'L\'Oréal Ecuador',
            'descripcion': 'Distribuidor oficial de productos L\'Oréal',
            'telefono': '+593-2-123-4567',
            'pais': 'Ecuador',
            'correo': 'contacto@loreal.ec',
            'direccion': 'Av. Amazonas 456, Quito'
        }
    
    def test_proveedor_creation_with_valid_data(self):
        """Test creating supplier with valid data"""
        proveedor = Proveedor.objects.create(**self.valid_data)
        self.assertEqual(proveedor.nombre, 'L\'Oréal Ecuador')
        self.assertEqual(proveedor.pais, 'Ecuador')
        self.assertEqual(proveedor.correo, 'contacto@loreal.ec')
    
    def test_proveedor_string_representation(self):
        """Test the string representation of supplier"""
        proveedor = Proveedor.objects.create(**self.valid_data)
        self.assertEqual(str(proveedor), 'L\'Oréal Ecuador')
    
    def test_proveedor_email_validation(self):
        """Test email validation for supplier"""
        invalid_data = self.valid_data.copy()
        invalid_data['correo'] = 'invalid-email'
        
        proveedor = Proveedor(**invalid_data)
        with self.assertRaises(ValidationError):
            proveedor.full_clean()


class ModelIntegrationTest(TestCase):
    """Integration tests for model relationships and constraints"""
    
    def test_all_models_can_be_created_together(self):
        """Test that all models can coexist without conflicts"""
        # Create one of each model
        trabajador = Trabajador.objects.create(
            nombre='María', apellido='López', correo='maria@test.com',
            cedula='123456789', codigo_empleado='EMP001'
        )
        
        empresa = Empresa.objects.create(
            nombre='Test Company', direccion='Test Address',
            mision='Test Mission', vision='Test Vision',
            anio_fundacion=2020, ruc='1234567890123'
        )
        
        producto = Producto.objects.create(
            nombre='Test Product', descripcion='Test Description',
            precio=10.99, iva=15
        )
        
        proveedor = Proveedor.objects.create(
            nombre='Test Supplier', descripcion='Test Supplier Desc',
            telefono='123456789', pais='Ecuador',
            correo='supplier@test.com', direccion='Supplier Address'
        )
        
        # Verify all were created
        self.assertEqual(Trabajador.objects.count(), 1)
        self.assertEqual(Empresa.objects.count(), 1)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Proveedor.objects.count(), 1)
    
    def test_database_constraints_enforcement(self):
        """Test that database constraints are properly enforced"""
        # Test unique constraints across different models
        Trabajador.objects.create(
            nombre='Test', apellido='User', correo='test@same.com',
            cedula='111', codigo_empleado='EMP111'
        )
        
        # Different model can have same email (if not globally unique)
        Proveedor.objects.create(
            nombre='Test Supplier', descripcion='Desc',
            telefono='123', pais='Ecuador',
            correo='test@same.com', direccion='Address'
        )
        
        self.assertEqual(Trabajador.objects.filter(correo='test@same.com').count(), 1)
        self.assertEqual(Proveedor.objects.filter(correo='test@same.com').count(), 1)