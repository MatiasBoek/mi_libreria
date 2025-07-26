from django.urls import path
from .views import inicio, agregar_datos, agregar_autor, agregar_libro, buscar

app_name = 'gestion_libros'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('agregar/<str:modelo>/', agregar_datos, name='agregar'),
    path('agregar/autor/', agregar_autor, name='agregar_autor'),
    path('agregar/libro/', agregar_libro, name='agregar_libro'),
    path('buscar/', buscar, name='buscar'),
]