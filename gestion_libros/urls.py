from django.urls import path
from . import views

app_name = 'gestion_libros'  # Namespace importante

urlpatterns = [
    path('agregar/autor/', views.agregar_autor, name='agregar_autor'),
    path('agregar/libro/', views.agregar_libro, name='agregar_libro'),
    path('', views.inicio, name='inicio'),  
    path('buscar/', views.buscar, name='buscar'),
]