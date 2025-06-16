"""
Test fixtures for Trabajador model using Factory pattern.
London School TDD approach with comprehensive test data generation.
"""
import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from apps.trabajadores.models import Trabajador
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


class TrabajadorFactory(DjangoModelFactory):
    """Factory for creating Trabajador test instances."""
    
    class Meta:
        model = Trabajador
    
    nombre = Faker('first_name', locale='es_ES')
    apellido = Faker('last_name', locale='es_ES') 
    correo = Faker('email')
    cedula = Faker('numerify', text='##########')
    codigo_empleado = Faker('numerify', text='EMP####')
    imagen = factory.LazyAttribute(lambda _: TrabajadorFactory._create_test_image())
    
    @staticmethod
    def _create_test_image():
        """Create a test image for trabajador."""
        image = Image.new('RGB', (100, 100), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='trabajador_test.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )


class TrabajadorTestData:
    """Test data provider for Trabajador model."""
    
    @staticmethod
    def valid_data():
        """Valid data for creating trabajador."""
        return {
            'nombre': 'María',
            'apellido': 'González',
            'correo': 'maria.gonzalez@cosmeticos.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001',
            'imagen': TrabajadorFactory._create_test_image()
        }
    
    @staticmethod
    def invalid_data():
        """Invalid data for testing validation."""
        return {
            'nombre': '',  # Required field empty
            'apellido': 'González',
            'correo': 'invalid-email',  # Invalid email format
            'cedula': '123',  # Too short
            'codigo_empleado': '',  # Required field empty
        }
    
    @staticmethod
    def update_data():
        """Data for update operations."""
        return {
            'nombre': 'María Carmen',
            'apellido': 'González Pérez',
            'correo': 'maria.carmen@cosmeticos.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001',
        }