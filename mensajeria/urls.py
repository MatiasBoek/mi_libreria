from django.urls import path
from . import views

app_name = 'mensajeria'

urlpatterns = [
    # Lista de conversaciones
    path('', views.lista_conversaciones, name='lista_conversaciones'),
    
    # Crear nueva conversación con un usuario específico
    path('nueva/<int:user_id>/', views.nueva_conversacion, name='nueva_conversacion'),
    
    # Detalle de conversación (dos patrones equivalentes, elimina uno)
    path('<int:conversacion_id>/', views.detalle_conversacion, name='detalle_conversacion'),
    
    # Enviar mensajes (versión simplificada)
    path('enviar/', views.enviar_mensaje, name='enviar_mensaje'),  # Formulario vacío
    path('enviar/usuario/<int:destinatario_id>/', views.enviar_mensaje, name='enviar_mensaje_usuario'),
    path('enviar/conversacion/<int:conversacion_id>/', views.enviar_mensaje, name='enviar_mensaje_conversacion'),

]


