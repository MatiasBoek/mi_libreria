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
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_envio']
