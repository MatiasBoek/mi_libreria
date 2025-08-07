from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversacion, Mensaje
from .forms import MensajeForm, EnviarMensajeForm
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

@login_required
def lista_conversaciones(request):
    conversaciones = request.user.conversaciones.all().order_by('-ultima_actualizacion')
    
    conversaciones_data = []
    for conversacion in conversaciones:
        destinatario = conversacion.participantes.exclude(id=request.user.id).first()
        conversaciones_data.append({
            'conversacion': conversacion,
            'destinatario': destinatario,
            'ultimo_mensaje': conversacion.mensajes.last(),
            'count_mensajes': conversacion.mensajes.count()
        })
    
    return render(request, 'mensajeria/lista.html', {
        'conversaciones_data': conversaciones_data,
        'breadcrumbs': [{'name': 'Mensajería', 'url': ''}]
    })

@login_required
def nueva_conversacion(request, user_id):
    destinatario = get_object_or_404(User, id=user_id)
    
    if request.user == destinatario:
        messages.error(request, "No puedes iniciar una conversación contigo mismo")
        return redirect('mensajeria:lista_conversaciones')
    
    conversacion = Conversacion.objects.filter(
        participantes=request.user
    ).filter(
        participantes=destinatario
    ).first()
    
    if not conversacion:
        conversacion = Conversacion.objects.create()
        conversacion.participantes.add(request.user, destinatario)
        messages.success(request, f"Nueva conversación con {destinatario.username}")
    else:
        messages.info(request, f"Conversación existente con {destinatario.username}")
    
    return redirect('mensajeria:detalle_conversacion', conversacion_id=conversacion.id)

@login_required
def detalle_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
    destinatario = conversacion.participantes.exclude(id=request.user.id).first()
    
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('inicio:inicio')},
        {'name': 'Mensajería', 'url': reverse('mensajeria:lista_conversaciones')},
        {'name': f'Chat con {destinatario.username}', 'url': ''},
    ]
    
    mensajes = conversacion.mensajes.all().order_by('fecha_envio')
    
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.conversacion = conversacion
            mensaje.remitente = request.user
            mensaje.destinatario = destinatario
            mensaje.save()
            
            conversacion.ultima_actualizacion = mensaje.fecha_envio
            conversacion.save()
            
            messages.success(request, "Mensaje enviado con éxito")
            return redirect('mensajeria:detalle_conversacion', conversacion_id=conversacion.id)
    else:
        form = MensajeForm()
    
    return render(request, 'mensajeria/detalle.html', {
        'conversacion': conversacion,
        'mensajes': mensajes,
        'form': form,
        'destinatario': destinatario,
        'breadcrumbs': breadcrumbs
    })
    
def procesar_mensaje_valido(request, form, destinatario, conversacion):
    """Función auxiliar para procesar mensajes válidos"""
    if isinstance(form, EnviarMensajeForm):
        
        destinatario = form.cleaned_data['destinatario']
        contenido = form.cleaned_data['contenido']
        mensaje = Mensaje(contenido=contenido)
    else:
      
        mensaje = form.save(commit=False)
    
    mensaje.remitente = request.user
    mensaje.destinatario = destinatario
    
    if conversacion:
        mensaje.conversacion = conversacion
    else:
        # Crear nueva conversación si no existe
        conversacion = Conversacion.objects.create()
        conversacion.participantes.add(request.user, destinatario)
        mensaje.conversacion = conversacion
    
    mensaje.save()
    
    conversacion.ultima_actualizacion = timezone.now()
    conversacion.save()
    
    messages.success(request, "Mensaje enviado con éxito")
    return redirect('mensajeria:detalle_conversacion', conversacion_id=mensaje.conversacion.id)

@login_required
def enviar_mensaje(request, destinatario_id=None, conversacion_id=None):
    breadcrumbs = [
        {'name': 'Mensajería', 'url': reverse('mensajeria:lista_conversaciones')},
        {'name': 'Nuevo mensaje', 'url': ''}
    ]

    try:
        destinatario = None
        conversacion = None
        form_class = MensajeForm  # Por defecto usamos MensajeForm

        # Manejo de destinatario específico
        if destinatario_id:
            destinatario = get_object_or_404(User, id=destinatario_id)
            breadcrumbs[2]['name'] = f'Nuevo mensaje a {destinatario.username}'
        
        # Manejo de conversación existente
        elif conversacion_id:
            conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
            destinatario = conversacion.participantes.exclude(id=request.user.id).first()
            breadcrumbs[2]['name'] = f'Responder a {destinatario.username}'
        
        # Si no hay destinatario ni conversación, mostramos el formulario completo
        else:
            form_class = EnviarMensajeForm

        if request.method == 'POST':
            form = form_class(request.POST, user=request.user)
            if form.is_valid():
                return procesar_mensaje_valido(request, form, destinatario, conversacion)
        else:
            form = form_class(user=request.user)
            # Si tenemos destinatario en el contexto pero usamos EnviarMensajeForm
            if destinatario and isinstance(form, EnviarMensajeForm):
                form.fields['destinatario'].initial = destinatario

        return render(request, 'mensajeria/enviar_mensaje.html', {
            'form': form,
            'destinatario': destinatario,
            'conversacion': conversacion,
            'breadcrumbs': breadcrumbs
        })

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return redirect('mensajeria:lista_conversaciones')