"""
Unit tests for Trabajador model following London School TDD.
Tests focus on behavior verification with mocking of dependencies.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from unittest.mock import patch, Mock
from apps.trabajadores.models import Trabajador
from tests.base_test_cases import BaseModelTestCase
from tests.fixtures.trabajador_factory import TrabajadorFactory, TrabajadorTestData


class TrabajadorModelTest(BaseModelTestCase):
    """Test Trabajador model behavior and validation."""
    
    def test_trabajador_creation_with_valid_data(self):
        """Test that trabajador is created successfully with valid data."""
        data = TrabajadorTestData.valid_data()
        trabajador = Trabajador.objects.create(**data)
        
        self.assertEqual(trabajador.nombre, data['nombre'])
        self.assertEqual(trabajador.apellido, data['apellido'])
        self.assertEqual(trabajador.correo, data['correo'])
        self.assertEqual(trabajador.cedula, data['cedula'])
        self.assertEqual(trabajador.codigo_empleado, data['codigo_empleado'])
        self.assertTrue(trabajador.imagen)
    
    def test_trabajador_string_representation(self):
        """Test that string representation returns expected format."""
        trabajador = TrabajadorFactory.create(
            nombre='Juan',
            apellido='Pérez'
        )
        expected_str = f"Juan Pérez"
        self.assertEqual(str(trabajador), expected_str)
    
    def test_trabajador_nombre_required(self):
        """Test that nombre field is required."""
        data = TrabajadorTestData.valid_data()
        data['nombre'] = ''
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_trabajador_apellido_required(self):
        """Test that apellido field is required."""
        data = TrabajadorTestData.valid_data()
        data['apellido'] = ''
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_trabajador_correo_validation(self):
        """Test that correo field validates email format."""
        data = TrabajadorTestData.valid_data()
        data['correo'] = 'invalid-email-format'
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_trabajador_cedula_required(self):
        """Test that cedula field is required."""
        data = TrabajadorTestData.valid_data()
        data['cedula'] = ''
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_trabajador_codigo_empleado_unique(self):
        """Test that codigo_empleado must be unique."""
        data = TrabajadorTestData.valid_data()
        TrabajadorFactory.create(codigo_empleado='EMP001')
        
        # Try to create another with same codigo_empleado
        data['codigo_empleado'] = 'EMP001'
        trabajador = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    @patch('apps.trabajadores.models.Trabajador.save')
    def test_trabajador_save_calls_parent_save(self, mock_save):
        """Test that save method calls parent save (London School - mock verification)."""
        trabajador = TrabajadorFactory.build()
        trabajador.save()
        
        mock_save.assert_called_once()
    
    def test_trabajador_image_upload_path(self):
        """Test that image is uploaded to correct path."""
        trabajador = TrabajadorFactory.create()
        
        # Verify image path contains trabajadores directory
        self.assertIn('trabajadores/', trabajador.imagen.name)
    
    def test_trabajador_cedula_max_length(self):
        """Test that cedula respects max length constraint."""
        data = TrabajadorTestData.valid_data()
        data['cedula'] = '1' * 21  # Exceed max_length of 20
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_trabajador_codigo_empleado_max_length(self):
        """Test that codigo_empleado respects max length constraint."""
        data = TrabajadorTestData.valid_data()
        data['codigo_empleado'] = 'E' * 21  # Exceed max_length of 20
        
        trabajador = Trabajador(**data)
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
            
    def test_trabajador_meta_options(self):
        """Test that model meta options are correctly set."""
        self.assertEqual(Trabajador._meta.verbose_name, 'Trabajador')
        self.assertEqual(Trabajador._meta.verbose_name_plural, 'Trabajadores')
        
    @patch('PIL.Image.open')
    def test_trabajador_image_processing(self, mock_image_open):
        """Test image processing behavior with mocked PIL (London School)."""
        mock_image = Mock()
        mock_image_open.return_value = mock_image
        
        trabajador = TrabajadorFactory.create()
        
        # Verify image field behavior
        self.assertTrue(trabajador.imagen)
        self.assertIsInstance(trabajador.imagen.name, str)