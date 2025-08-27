from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversacion(models.Model):
    participantes = models.ManyToManyField(User, related_name='conversaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ultima_actualizacion']

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_envio']
