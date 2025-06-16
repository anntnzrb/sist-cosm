from django.urls import path
from . import views

app_name = 'trabajadores'

urlpatterns = [
    path('', views.TrabajadorListView.as_view(), name='list'),
    path('create/', views.TrabajadorCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TrabajadorUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TrabajadorDeleteView.as_view(), name='delete'),
]