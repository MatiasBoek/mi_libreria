from django import forms
from .models import Autor, Editorial, Libro, Resena

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'fecha_fallecimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'biografia': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Ingrese una breve biografía del autor...'
            }),
        }
        labels = {
            'nombre': 'Nombre del Autor',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'fecha_fallecimiento': 'Fecha de Fallecimiento (opcional)',
            'nacionalidad': 'Nacionalidad',
            'biografia': 'Biografía'
        }
        help_texts = {
            'fecha_fallecimiento': 'Dejar en blanco si el autor aún vive'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extrae el request primero
        super().__init__(*args, **kwargs)
        
        # Añade clases Bootstrap y placeholders
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            if field_name not in ['fecha_nacimiento', 'fecha_fallecimiento'] and not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = f'Ingrese {self.fields[field_name].label.lower()}...'
            
            # Mejora para campos booleanos si los tienes
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        if self.request and not self.request.user.is_authenticated:
            raise forms.ValidationError("Debes estar autenticado para realizar esta acción")
        return cleaned_data 

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.admin_user = kwargs.pop('admin_user', False)
        super().__init__(*args, **kwargs)
        
        if not self.admin_user:
            for field_name in self.fields:
                if field_name != 'logo':  
                    self.fields[field_name].disabled = True

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-select'}),
            'editorial': forms.Select(attrs={'class': 'form-select'}),
            'año_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'paginas': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'portada': forms.FileInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titulo': 'Título del libro',
            'año_publicacion': 'Año de publicación',
            'descripcion': 'Descripción/Reseña',
        }
            
# BLOG

class BusquedaForm(forms.Form):
    termino = forms.CharField(
        label='Buscar',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese término de búsqueda'
        })
    )
    
class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['contenido', 'calificacion', 'libro', 'usuario']  
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu reseña aquí...'
            }),
            'calificacion': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'libro': forms.HiddenInput(),
            'usuario': forms.HiddenInput()
        }
        labels = {
            'contenido': 'Tu reseña',
            'calificacion': 'Calificación (1-5)'
        }
