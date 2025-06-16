from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='list'),
    path('create/', views.ProductoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='delete'),
]