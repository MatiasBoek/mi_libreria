from django import forms
from .models import Mensaje
from django.contrib.auth import get_user_model

User = get_user_model()

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe tu mensaje aquí...'
            }),
        }

class EnviarMensajeForm(forms.Form):
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Para",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...'
        }),
        label="Mensaje"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['destinatario'].queryset = User.objects.exclude(id=user.id)