"""
End-to-end integration tests for the complete application.
Tests the full user workflows and system integration.
"""

from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from apps.empresa.models import Empresa
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.trabajadores.models import Trabajador


class EndToEndIntegrationTest(TestCase):
    """Complete end-to-end integration tests"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_complete_cosmetics_store_workflow(self):
        """Test the complete workflow of the cosmetics store application"""

        # 1. Start at homepage
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cosmetics Store")

        # 2. Navigate to "Nosotros" page (should show no company info initially)
        response = self.client.get(reverse("empresa:detail"))
        self.assertEqual(response.status_code, 200)

        # 3. Create company information
        empresa_data = {
            "nombre": "Bella Cosmetics Ecuador",
            "direccion": "Av. República del Salvador N34-183, Quito",
            "mision": "Ofrecer productos de belleza de la más alta calidad para realzar la belleza natural de nuestros clientes",
            "vision": "Ser la tienda de cosméticos líder en Ecuador, reconocida por la excelencia en servicio y productos",
            "anio_fundacion": 2015,
            "ruc": "1791234567001",
        }

        response = self.client.post(reverse("empresa:create"), data=empresa_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation

        # Verify company was created
        empresa = Empresa.objects.get()
        self.assertEqual(empresa.nombre, "Bella Cosmetics Ecuador")

        # 4. Add team members (trabajadores)
        trabajadores_data = [
            {
                "nombre": "Sofia",
                "apellido": "Morales",
                "correo": "sofia.morales@bella-cosmetics.ec",
                "cedula": "1723456789",
                "codigo_empleado": "EMP001",
            },
            {
                "nombre": "Carmen",
                "apellido": "Vásquez",
                "correo": "carmen.vasquez@bella-cosmetics.ec",
                "cedula": "1734567890",
                "codigo_empleado": "EMP002",
            },
            {
                "nombre": "Isabella",
                "apellido": "Herrera",
                "correo": "isabella.herrera@bella-cosmetics.ec",
                "cedula": "1745678901",
                "codigo_empleado": "EMP003",
            },
        ]

        for trabajador_data in trabajadores_data:
            response = self.client.post(
                reverse("trabajadores:create"), data=trabajador_data
            )
            self.assertEqual(response.status_code, 302)

        # Verify workers were created
        self.assertEqual(Trabajador.objects.count(), 3)

        # 5. Add product catalog
        productos_data = [
            {
                "nombre": "Lápiz Labial Matte Rouge",
                "descripcion": "Lápiz labial de larga duración con acabado mate y color intenso",
                "precio": "28.99",
                "iva": 15,
            },
            {
                "nombre": "Base de Maquillaje Natural Cover",
                "descripcion": "Base líquida con cobertura natural para todo tipo de piel",
                "precio": "45.50",
                "iva": 15,
            },
            {
                "nombre": "Paleta de Sombras Sunset",
                "descripcion": "Paleta de 12 sombras con tonos cálidos y acabados variados",
                "precio": "65.00",
                "iva": 15,
            },
            {
                "nombre": "Serum Facial Antioxidante",
                "descripcion": "Serum con vitamina C para cuidado facial diario",
                "precio": "89.99",
                "iva": 0,  # Productos de cuidado facial sin IVA
            },
        ]

        for producto_data in productos_data:
            response = self.client.post(reverse("productos:create"), data=producto_data)
            self.assertEqual(response.status_code, 302)

        # Verify products were created (4 new + 10 sample products from migration)
        self.assertEqual(Producto.objects.count(), 14)

        # 6. Add suppliers
        proveedores_data = [
            {
                "nombre": "L'Oréal Ecuador S.A.",
                "descripcion": "Distribuidor oficial de productos L'Oréal en Ecuador",
                "telefono": "+593-2-234-5678",
                "pais": "Ecuador",
                "correo": "contacto@loreal.com.ec",
                "direccion": "Av. Amazonas N21-147, Quito",
            },
            {
                "nombre": "Maybelline International",
                "descripcion": "Proveedor global de productos de maquillaje Maybelline",
                "telefono": "+1-212-573-5000",
                "pais": "Estados Unidos",
                "correo": "wholesale@maybelline.com",
                "direccion": "200 Madison Avenue, New York, NY 10016",
            },
            {
                "nombre": "Natura Cosméticos",
                "descripcion": "Empresa brasileña especializada en cosméticos naturales",
                "telefono": "+55-11-4444-3000",
                "pais": "Brasil",
                "correo": "comercial@natura.com.br",
                "direccion": "Rua Dr. Cardoso de Melo, 1466, São Paulo",
            },
        ]

        for proveedor_data in proveedores_data:
            response = self.client.post(
                reverse("proveedores:create"), data=proveedor_data
            )
            self.assertEqual(response.status_code, 302)

        # Verify suppliers were created
        self.assertEqual(Proveedor.objects.count(), 3)

        # 7. Test navigation between all sections
        navigation_urls = [
            ("home", "Cosmetics Store"),
            ("empresa:detail", "Bella Cosmetics Ecuador"),
            ("trabajadores:list", "NUESTRO PERSONAL"),
            ("productos:list", "NUESTROS PRODUCTOS"),
            ("proveedores:list", "NUESTROS PROVEEDORES"),
        ]

        for url_name, expected_content in navigation_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, expected_content)

        # 8. Test updating records
        # Update company information
        updated_empresa_data = empresa_data.copy()
        updated_empresa_data["nombre"] = "Bella Cosmetics Ecuador Premium"

        response = self.client.post(
            reverse("empresa:update"), data=updated_empresa_data
        )
        # Handle both redirect and form re-display cases
        self.assertIn(response.status_code, [200, 302])

        empresa.refresh_from_db()
        self.assertEqual(empresa.nombre, "Bella Cosmetics Ecuador Premium")

        # Update a worker
        trabajador = Trabajador.objects.filter(cedula="1723456789").first()
        updated_trabajador_data = {
            "nombre": "Sofia María",
            "apellido": "Morales",
            "correo": "sofia.morales@bella-cosmetics.ec",
            "cedula": "1723456789",
            "codigo_empleado": "EMP001",
        }

        response = self.client.post(
            reverse("trabajadores:update", kwargs={"pk": trabajador.pk}),
            data=updated_trabajador_data,
        )
        # Handle both redirect and form re-display cases
        self.assertIn(response.status_code, [200, 302])

        trabajador.refresh_from_db()
        self.assertEqual(trabajador.nombre, "Sofia María")

        # 9. Test business logic
        # Verify IVA calculations work correctly
        producto_con_iva = Producto.objects.filter(iva=15).first()
        precio_con_iva = producto_con_iva.get_precio_con_iva()
        expected_price = float(producto_con_iva.precio) * 1.15
        self.assertAlmostEqual(float(precio_con_iva), expected_price, places=2)

        # 10. Test data integrity
        # Verify unique constraints work
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Trabajador.objects.create(
                    nombre="Duplicate",
                    apellido="Worker",
                    correo="duplicate@test.com",
                    cedula="1723456789",  # Same cedula as existing worker
                    codigo_empleado="EMP999",
                )

        # 11. Test deletion workflow
        # Delete a product
        producto_to_delete = Producto.objects.last()
        response = self.client.post(
            reverse("productos:delete", kwargs={"pk": producto_to_delete.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Producto.objects.count(), 13)  # One less product (14 - 1)

        # 12. Final verification - all sections should still be accessible
        for url_name, _ in navigation_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_cosmetics_store_data_consistency(self):
        """Test data consistency across the application"""

        # Create test data
        empresa = Empresa.objects.create(
            nombre="Cosmetics Test Store",
            direccion="Test Address",
            mision="Test Mission",
            vision="Test Vision",
            anio_fundacion=2020,
            ruc="9999999999999",
        )

        trabajador = Trabajador.objects.create(
            nombre="Test",
            apellido="Employee",
            correo="test@employee.com",
            cedula="9999999999",
            codigo_empleado="TEST001",
        )

        producto = Producto.objects.create(
            nombre="Test Product", descripcion="Test Description", precio=50.00, iva=15
        )

        proveedor = Proveedor.objects.create(
            nombre="Test Supplier",
            descripcion="Test Supplier Description",
            telefono="123456789",
            pais="Test Country",
            correo="test@supplier.com",
            direccion="Test Supplier Address",
        )

        # Test that all models exist and have correct data
        self.assertEqual(Empresa.objects.count(), 1)
        self.assertEqual(Trabajador.objects.count(), 1)
        self.assertEqual(Producto.objects.count(), 11)  # 1 created + 10 sample products
        self.assertEqual(Proveedor.objects.count(), 1)

        # Test string representations
        self.assertEqual(str(empresa), "Cosmetics Test Store")
        self.assertEqual(str(trabajador), "Test Employee")
        self.assertEqual(str(producto), "Test Product")
        self.assertEqual(str(proveedor), "Test Supplier")

        # Test business logic
        self.assertAlmostEqual(
            float(producto.get_precio_con_iva()), 57.50, places=2
        )  # 50 + 15%

        # Test empresa singleton constraint
        with self.assertRaises(Exception):
            Empresa.objects.create(
                nombre="Second Company",
                direccion="Another Address",
                mision="Another Mission",
                vision="Another Vision",
                anio_fundacion=2021,
                ruc="8888888888888",
            )

    def test_cosmetics_theme_and_ui_consistency(self):
        """Test that the cosmetics theme is consistently applied"""

        # Test all main pages load with proper cosmetics branding
        pages_to_test = [
            reverse("home"),
            reverse("empresa:detail"),
            reverse("trabajadores:list"),
            reverse("productos:list"),
            reverse("proveedores:list"),
        ]

        for url in pages_to_test:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            # Check for cosmetics branding elements
            self.assertContains(response, "Cosmetics Store")
            self.assertContains(response, "cosmetics-theme.css")

            # Check for Bootstrap framework
            self.assertContains(response, "bootstrap")

        # Check FontAwesome icons on pages that use them (not home page after refactoring)
        pages_with_icons = [
            reverse("productos:list"),
            reverse("trabajadores:list"),
            reverse("proveedores:list"),
        ]

        for url in pages_with_icons:
            response = self.client.get(url)
            self.assertContains(response, "fa-")  # FontAwesome icons

    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases"""

        # Test accessing non-existent records
        response = self.client.get(reverse("trabajadores:update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("productos:delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)

        # Test invalid form submissions
        invalid_trabajador_data = {
            "nombre": "",  # Required field empty
            "correo": "invalid-email",
            "cedula": "not-numbers",
        }

        response = self.client.post(
            reverse("trabajadores:create"), data=invalid_trabajador_data
        )
        self.assertEqual(response.status_code, 200)  # Should stay on form page
        self.assertContains(response, "form")

        # Test empresa singleton behavior
        # First, ensure no company exists
        Empresa.objects.all().delete()

        # Access empresa detail page - should show "no info" template
        response = self.client.get(reverse("empresa:detail"))
        self.assertEqual(response.status_code, 200)

        # Create a company
        empresa_data = {
            "nombre": "Test Company",
            "direccion": "Test Address",
            "mision": "Test Mission",
            "vision": "Test Vision",
            "anio_fundacion": 2020,
            "ruc": "1111111111111",
        }

        response = self.client.post(reverse("empresa:create"), data=empresa_data)
        self.assertEqual(response.status_code, 302)

        # Now access the create page again - should redirect to detail
        response = self.client.get(reverse("empresa:create"))
        self.assertEqual(response.status_code, 302)  # Redirect because company exists
