from django.urls import path

from . import views

app_name = "empresa"

urlpatterns = [
    path("", views.EmpresaView.as_view(), name="detail"),
    path("create/", views.EmpresaCreateView.as_view(), name="create"),
    path("update/", views.EmpresaUpdateView.as_view(), name="update"),
]
