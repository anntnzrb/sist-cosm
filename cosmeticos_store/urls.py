"""
URL configuration for cosmeticos_store project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("nosotros/", include("apps.empresa.urls")),
    path("trabajadores/", include("apps.trabajadores.urls")),
    path("productos/", include("apps.productos.urls")),
    path("proveedores/", include("apps.proveedores.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
