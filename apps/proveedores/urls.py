from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.ProveedorListView.as_view(), name='list'),
    path('create/', views.ProveedorCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProveedorUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProveedorDeleteView.as_view(), name='delete'),
]