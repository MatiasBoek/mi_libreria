from django.urls import path
from . import views

app_name = 'inicio'  # Namespace

urlpatterns = [
    path('agregar/autor/', views.agregar_autor, name='agregar_autor'),
    path('agregar/libro/', views.agregar_libro, name='agregar_libro'),
    path('', views.inicio, name='inicio'),  
    path('buscar/', views.buscar, name='buscar'),
    path('agregar/<str:modelo>/', views.agregar_datos, name='agregar'),    
    path('libros/', views.listar_libros, name='listar_libros'),
    path('autores/', views.listar_autores, name='listar_autores'),
    path('editoriales/', views.listar_editoriales, name='listar_editoriales'),
    path('contact/', views.contacto, name='contacto'),
]