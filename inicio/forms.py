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
        super().__init__(*args, **kwargs)
        # Añade clases Bootstrap y placeholders
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            if field_name != 'fecha_nacimiento' and not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = f'Ingrese {field.label.lower()}...'
            
            # Mejora para campos booleanos si los tienes
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'   

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Penguin Random House'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Argentina'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: https://www.penguinrandomhouse.com/'
            }),
            'fundacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1500',
                'max': '2025'  # Año actual
            }),
        }
        labels = {
            'nombre': 'Nombre de la editorial',
            'pais': 'País de origen',
            'sitio_web': 'Sitio web oficial',
            'fundacion': 'Año de fundación'
        }

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

class BusquedaForm(forms.Form):
    termino_busqueda = forms.CharField(label='Buscar', max_length=100)
    
# BLOG


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['tipo', 'libro', 'autor', 'editorial', 'titulo', 'contenido', 'puntuacion']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].required = False
        self.fields['autor'].required = False
        self.fields['editorial'].required = False
