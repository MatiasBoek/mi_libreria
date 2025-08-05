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
    path('libros/<int:libro_id>/resena/', views.crear_resena, name='crear_resena'),
    
    # URLs para Editoriales
    path('editoriales/', views.listar_editoriales, name='listar_editoriales'),
    path('editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    path('editoriales/detalle/<int:pk>/', views.detalle_editorial, name='detalle_editorial'),
    path('editoriales/editar/<int:pk>/', views.editar_editorial, name='editar_editorial'),
    path('editoriales/eliminar/<int:pk>/', views.eliminar_editorial, name='eliminar_editorial'),
    
    # Contacto
    path('contacto/', views.contacto, name='contacto'),
    
    # Sobre mi
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    
    #Blog
    path('resenas/', views.listar_resenas, name='listar_resenas'),
    path('resenas/nueva/', views.crear_resena, name='crear_resena'),
    path('resenas/<int:pk>/', views.detalle_resena, name='detalle_resena'),
    path('mis-resenas/', views.mis_resenas, name='mis_resenas'),
    
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-exito/', views.logout_exito_view, name='logout_exito'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Password reset URLs
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='inicio/password_reset.html',
        email_template_name='inicio/password_reset_email.html',
        subject_template_name='inicio/password_reset_subject.txt',
        success_url='/login/'
    ), name='password_reset'),
    
    path('recuperar-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='inicio/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('restablecer/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='inicio/password_reset_confirm.html',
        success_url='/recuperar-contrasena/completado/'
    ), name='password_reset_confirm'),
    
    path('recuperar-contrasena/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='inicio/password_reset_complete.html'
    ), name='password_reset_complete'),
        
    path('pages/', views.listar_paginas, name='listar_paginas'),
    path('pages/<int:pk>/', views.detalle_pagina, name='detalle_pagina'),
    
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
]