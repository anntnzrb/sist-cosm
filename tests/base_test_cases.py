"""
Base test cases following London School TDD methodology.
Provides common patterns and utilities for comprehensive testing.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch
import tempfile
from PIL import Image
import io


class BaseModelTestCase(TestCase):
    """Base test case for model testing with London School approach."""
    
    def setUp(self):
        self.client = Client()
        
    def create_test_image(self, name="test.jpg", size=(100, 100)):
        """Create a test image for upload testing."""
        image = Image.new('RGB', size, color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name=name,
            content=image_file.read(),
            content_type='image/jpeg'
        )
    
    def assert_model_validation_error(self, model_instance, field_name, expected_error):
        """Assert that model validation raises expected error."""
        with self.assertRaises(Exception) as context:
            model_instance.full_clean()
        self.assertIn(expected_error, str(context.exception))


class BaseCRUDTestCase(BaseModelTestCase):
    """Base test case for CRUD operations testing."""
    
    model = None
    create_url = None
    list_url = None
    update_url_pattern = None
    delete_url_pattern = None
    
    def get_valid_data(self):
        """Override in subclasses to provide valid test data."""
        raise NotImplementedError("Subclasses must implement get_valid_data")
    
    def get_invalid_data(self):
        """Override in subclasses to provide invalid test data."""
        raise NotImplementedError("Subclasses must implement get_invalid_data")
    
    def test_create_view_get(self):
        """Test GET request to create view returns form."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_create_view_post_valid_data(self):
        """Test POST with valid data creates object and redirects."""
        initial_count = self.model.objects.count()
        response = self.client.post(self.create_url, self.get_valid_data())
        
        self.assertEqual(self.model.objects.count(), initial_count + 1)
        self.assertEqual(response.status_code, 302)
    
    def test_create_view_post_invalid_data(self):
        """Test POST with invalid data shows form errors."""
        initial_count = self.model.objects.count()
        response = self.client.post(self.create_url, self.get_invalid_data())
        
        self.assertEqual(self.model.objects.count(), initial_count)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
    
    def test_list_view(self):
        """Test list view displays objects."""
        obj = self.model.objects.create(**self.get_valid_data())
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(obj))


class BaseIntegrationTestCase(TestCase):
    """Base test case for integration testing."""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_crud_workflow(self):
        """Test complete CRUD workflow end-to-end."""
        # Create
        create_data = self.get_valid_data()
        response = self.client.post(self.create_url, create_data)
        self.assertEqual(response.status_code, 302)
        
        # Read
        obj = self.model.objects.get(**self.get_lookup_data())
        response = self.client.get(self.list_url)
        self.assertContains(response, str(obj))
        
        # Update
        update_data = self.get_update_data()
        update_url = self.update_url_pattern.format(id=obj.id)
        response = self.client.post(update_url, update_data)
        self.assertEqual(response.status_code, 302)
        
        # Delete
        delete_url = self.delete_url_pattern.format(id=obj.id)
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.model.objects.filter(id=obj.id).exists())