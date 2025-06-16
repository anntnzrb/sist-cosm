"""
Test fixtures for Producto model using Factory pattern.
London School TDD approach with comprehensive test data generation.
"""
import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from apps.productos.models import Producto
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from decimal import Decimal


class ProductoFactory(DjangoModelFactory):
    """Factory for creating Producto test instances."""
    
    class Meta:
        model = Producto
    
    nombre = Faker('word')
    descripcion = Faker('text', max_nb_chars=200)
    precio = Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    iva = factory.Iterator([0, 15])  # Valid IVA values
    imagen = factory.LazyAttribute(lambda _: ProductoFactory._create_test_image())
    
    @staticmethod
    def _create_test_image():
        """Create a test image for producto."""
        image = Image.new('RGB', (200, 200), color='pink')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='producto_test.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )


class ProductoTestData:
    """Test data provider for Producto model."""
    
    @staticmethod
    def valid_data():
        """Valid data for creating producto."""
        return {
            'nombre': 'Labial Mate Premium',
            'descripcion': 'Labial de larga duración con acabado mate y colores vibrantes',
            'precio': Decimal('29.99'),
            'iva': 15,
            'imagen': ProductoFactory._create_test_image()
        }
    
    @staticmethod
    def invalid_data():
        """Invalid data for testing validation."""
        return {
            'nombre': '',  # Required field empty
            'descripcion': 'A' * 1000,  # Too long
            'precio': Decimal('-10.00'),  # Negative price
            'iva': 20,  # Invalid IVA value (only 0 or 15 allowed)
        }
    
    @staticmethod
    def update_data():
        """Data for update operations."""
        return {
            'nombre': 'Labial Mate Premium Gold',
            'descripcion': 'Labial de larga duración con acabado mate, nueva fórmula dorada',
            'precio': Decimal('34.99'),
            'iva': 15,
        }
    
    @staticmethod
    def zero_iva_data():
        """Valid data with zero IVA."""
        return {
            'nombre': 'Producto Sin IVA',
            'descripcion': 'Producto de prueba sin IVA',
            'precio': Decimal('15.00'),
            'iva': 0,
            'imagen': ProductoFactory._create_test_image()
        }