from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.filter
def obtener_destinatario(conversacion, usuario):
    """Filtro para obtener el destinatario de una conversación"""
    return conversacion.participantes.exclude(id=usuario.id).first()