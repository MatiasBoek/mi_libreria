from django import forms
from .models import Autor, Editorial, Libro

from django import forms
from .models import Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'  # Esto incluirá todos los campos del modelo
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade clases Bootstrap a todos los campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

class BusquedaForm(forms.Form):
    termino_busqueda = forms.CharField(label='Buscar', max_length=100)