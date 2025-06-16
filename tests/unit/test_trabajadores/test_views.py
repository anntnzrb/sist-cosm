"""
Unit tests for Trabajador views following London School TDD.
Tests focus on view behavior with extensive mocking.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse
from unittest.mock import patch, Mock, MagicMock
from apps.trabajadores.models import Trabajador
from apps.trabajadores.views import TrabajadorListView, TrabajadorCreateView
from tests.base_test_cases import BaseCRUDTestCase
from tests.fixtures.trabajador_factory import TrabajadorFactory, TrabajadorTestData


class TrabajadorViewsTest(BaseCRUDTestCase):
    """Test Trabajador views with London School TDD approach."""
    
    model = Trabajador
    create_url = '/trabajadores/create/'
    list_url = '/trabajadores/'
    update_url_pattern = '/trabajadores/update/{id}/'
    delete_url_pattern = '/trabajadores/delete/{id}/'
    
    def get_valid_data(self):
        """Return valid data for form submission."""
        return TrabajadorTestData.valid_data()
    
    def get_invalid_data(self):
        """Return invalid data for form submission."""
        return TrabajadorTestData.invalid_data()
    
    def get_lookup_data(self):
        """Return data for object lookup."""
        return {'codigo_empleado': 'EMP001'}
    
    def get_update_data(self):
        """Return data for update operations."""
        return TrabajadorTestData.update_data()


class TrabajadorListViewTest(TestCase):
    """Test TrabajadorListView with mocking."""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('trabajadores:list')
    
    @patch('apps.trabajadores.views.TrabajadorListView.get_queryset')
    def test_list_view_calls_get_queryset(self, mock_get_queryset):
        """Test that list view calls get_queryset method."""
        mock_queryset = Mock()
        mock_get_queryset.return_value = mock_queryset
        
        response = self.client.get(self.url)
        
        mock_get_queryset.assert_called_once()
        self.assertEqual(response.status_code, 200)
    
    @patch('apps.trabajadores.models.Trabajador.objects.all')
    def test_list_view_displays_all_trabajadores(self, mock_all):
        """Test that list view displays all trabajadores."""
        mock_trabajadores = [
            Mock(nombre='Juan', apellido='Pérez'),
            Mock(nombre='María', apellido='González')
        ]
        mock_all.return_value = mock_trabajadores
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        mock_all.assert_called_once()
    
    def test_list_view_uses_correct_template(self):
        """Test that list view uses correct template."""
        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'trabajadores/list.html')
        self.assertEqual(response.status_code, 200)
    
    @patch('apps.trabajadores.views.TrabajadorListView.get_context_data')
    def test_list_view_context_data(self, mock_get_context):
        """Test that list view includes correct context data."""
        mock_context = {'title': 'NUESTRO PERSONAL'}
        mock_get_context.return_value = mock_context
        
        response = self.client.get(self.url)
        
        mock_get_context.assert_called_once()
        self.assertEqual(response.status_code, 200)


class TrabajadorCreateViewTest(TestCase):
    """Test TrabajadorCreateView with mocking."""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('trabajadores:create')
    
    @patch('apps.trabajadores.forms.TrabajadorForm')
    def test_create_view_uses_correct_form(self, mock_form_class):
        """Test that create view uses correct form class."""
        mock_form = Mock()
        mock_form_class.return_value = mock_form
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
    
    @patch('apps.trabajadores.models.Trabajador.save')
    def test_create_view_saves_valid_form(self, mock_save):
        """Test that create view saves valid form data."""
        mock_save.return_value = None
        
        data = TrabajadorTestData.valid_data()
        response = self.client.post(self.url, data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
    
    @patch('apps.trabajadores.forms.TrabajadorForm.is_valid')
    def test_create_view_handles_invalid_form(self, mock_is_valid):
        """Test that create view handles invalid form submission."""
        mock_is_valid.return_value = False
        
        data = TrabajadorTestData.invalid_data()
        response = self.client.post(self.url, data)
        
        # Should return form with errors
        self.assertEqual(response.status_code, 200)
        mock_is_valid.assert_called_once()
    
    def test_create_view_uses_correct_template(self):
        """Test that create view uses correct template."""
        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'trabajadores/create.html')
        self.assertEqual(response.status_code, 200)
    
    @patch('apps.trabajadores.views.messages.success')
    def test_create_view_shows_success_message(self, mock_success):
        """Test that create view shows success message on valid submission."""
        data = TrabajadorTestData.valid_data()
        response = self.client.post(self.url, data)
        
        # Should call success message
        mock_success.assert_called_once()
        self.assertEqual(response.status_code, 302)


class TrabajadorUpdateViewTest(TestCase):
    """Test TrabajadorUpdateView with mocking."""
    
    def setUp(self):
        self.client = Client()
        self.trabajador = TrabajadorFactory.create()
        self.url = reverse('trabajadores:update', kwargs={'pk': self.trabajador.pk})
    
    @patch('apps.trabajadores.models.Trabajador.objects.get')
    def test_update_view_gets_correct_object(self, mock_get):
        """Test that update view retrieves correct object."""
        mock_get.return_value = self.trabajador
        
        response = self.client.get(self.url)
        
        mock_get.assert_called_once_with(pk=self.trabajador.pk)
        self.assertEqual(response.status_code, 200)
    
    @patch('apps.trabajadores.models.Trabajador.save')
    def test_update_view_saves_changes(self, mock_save):
        """Test that update view saves changes to object."""
        mock_save.return_value = None
        
        data = TrabajadorTestData.update_data()
        response = self.client.post(self.url, data)
        
        mock_save.assert_called_once()
        self.assertEqual(response.status_code, 302)


class TrabajadorDeleteViewTest(TestCase):
    """Test TrabajadorDeleteView with mocking."""
    
    def setUp(self):
        self.client = Client()
        self.trabajador = TrabajadorFactory.create()
        self.url = reverse('trabajadores:delete', kwargs={'pk': self.trabajador.pk})
    
    @patch('apps.trabajadores.models.Trabajador.delete')
    def test_delete_view_deletes_object(self, mock_delete):
        """Test that delete view deletes the object."""
        mock_delete.return_value = None
        
        response = self.client.post(self.url)
        
        mock_delete.assert_called_once()
        self.assertEqual(response.status_code, 302)
    
    @patch('apps.trabajadores.views.messages.success')
    def test_delete_view_shows_success_message(self, mock_success):
        """Test that delete view shows success message."""
        response = self.client.post(self.url)
        
        mock_success.assert_called_once()
        self.assertEqual(response.status_code, 302)