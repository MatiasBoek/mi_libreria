from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'inicio'  # Namespace

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar, name='buscar'),
    
    # URLs para Autores
    path('autores/', views.listar_autores, name='listar_autores'),
    path('autor/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),
    path('autor/editar/<int:pk>/', views.editar_autor, name='editar_autor'),
    
    # URLs para Libros
    path('libros/', views.listar_libros, name='listar_libros'),
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('libros/editar/<int:pk>/', views.editar_libro, name='editar_libro'),
    
    # URLs para Editoriales
    path('editoriales/', views.listar_editoriales, name='listar_editoriales'),
    path('editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    
    # Contacto
    path('contacto/', views.contacto, name='contacto'),
    
    # Sobre mi
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    
    #Blog
    path('resenas/', views.listar_resenas, name='listar_resenas'),
    path('resenas/nueva/', views.crear_resena, name='crear_resena'),
    path('resenas/<int:pk>/', views.detalle_resena, name='detalle_resena'),
    path('mis-resenas/', views.mis_resenas, name='mis_resenas'),
    
     # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
]