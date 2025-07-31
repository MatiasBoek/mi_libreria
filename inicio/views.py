from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Editorial, Libro
from .forms import AutorForm, EditorialForm, LibroForm, BusquedaForm
from django.contrib import messages

def inicio(request):
    return render(request, 'index.html')

# LIBRO

def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_libros:index')  # Ajusta este nombre según tus URLs
    else:
        form = LibroForm()
    
    return render(request, 'gestion_libros/agregar_libro.html', {'form': form})

def listar_libros(request):
    libros = Libro.objects.all().order_by('titulo') 
    context = {
        'libros': libros,
        'title': 'Lista de Libros'
    }
    return render(request, 'libros.html', context)

# AUTOR

def agregar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El autor se ha guardado con éxito.')
            return redirect('inicio:listar_autores') 
    else: 
        form = AutorForm()
        
    return render(request, 'gestion_libros/agregar_autor.html', {'form': form})


def listar_autores(request):
    autores = Autor.objects.all().order_by('apellido', 'nombre') # Obtener todos los autores
    context = {
        'autores': autores,
        'title': 'Lista de Autores'
    }
    return render(request, 'autores.html', context) 

   
def agregar_editorial(request):
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio:listar_editoriales')  
    else:
        form = EditorialForm()
    
    return render(request, 'gestion_libros/agregar_editorial.html', {'form': form})

def detalle_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    return render(request, 'gestion_libros/detalle_autor.html', {'autor': autor})

def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('inicio:detalle_autor', pk=autor.pk)
    else:
        form = AutorForm(instance=autor)
    
    return render(request, 'gestion_libros/editar_autor.html', {
        'form': form,
        'autor': autor
    })

# BUSCAR
def buscar(request):
    resultados = None
    if request.method == 'POST':
        form = BusquedaForm(request.POST)
        if form.is_valid():
            termino = form.cleaned_data['termino_busqueda']
            resultados = {
                'autores': Autor.objects.filter(nombre__icontains=termino),
                'editoriales': Editorial.objects.filter(nombre__icontains=termino),
                'libros': Libro.objects.filter(titulo__icontains=termino),
            }
    else:
        form = BusquedaForm()
    
    return render(request, 'gestion_libros/buscar.html', {'form': form, 'resultados': resultados})

#EDITORIAL

def listar_editoriales(request):
    editoriales = Editorial.objects.all().order_by('nombre') # Obtener todas las editoriales
    context = {
        'editoriales': editoriales,
        'title': 'Lista de Editoriales'
    }
    return render(request, 'editoriales.html', context) # Necesitarás crear esta plantilla

# CONTACTO
def contacto(request):
    """
    Vista para la página de contacto.
    """
    context = {
        'title': 'Contacto',
    }
    
    return render(request, 'contacto.html', context)


