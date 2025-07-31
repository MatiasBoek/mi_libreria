from django.shortcuts import render, redirect
from .models import Autor, Editorial, Libro
from .forms import AutorForm, EditorialForm, LibroForm, BusquedaForm

def inicio(request):
    return render(request, 'index.html')

def agregar_datos(request, modelo):
    if request.method == 'POST':
        if modelo == 'autor':
            form = AutorForm(request.POST)
        elif modelo == 'editorial':
            form = EditorialForm(request.POST)
        elif modelo == 'libro':
            form = LibroForm(request.POST)
            
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        if modelo == 'autor':
            form = AutorForm()
        elif modelo == 'editorial':
            form = EditorialForm()
        elif modelo == 'libro':
            form = LibroForm()
    
    return render(request, 'gestion_libros/agregar.html', {'form': form, 'modelo': modelo})

def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_libros:index')  # Ajusta este nombre según tus URLs
    else:
        form = LibroForm()
    
    return render(request, 'gestion_libros/agregar_libro.html', {'form': form})

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

def agregar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = AutorForm()
    return render(request, 'gestion_libros/agregar_autor.html', {'form': form})

def agregar_editorial(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        pais = request.POST.get('pais')
        sitio_web = request.POST.get('sitio_web')
        fundacion = request.POST.get('fundacion')
        
        Editorial.objects.create(
            nombre=nombre,
            pais=pais,
            sitio_web=sitio_web,
            fundacion=fundacion
        )
        return redirect('listar_editoriales')
    
    return render(request, 'agregar_editorial.html')

def listar_libros(request):
    libros = Libro.objects.all().order_by('titulo') # Obtener todos los libros
    context = {
        'libros': libros,
        'title': 'Lista de Libros'
    }
    return render(request, 'libros.html', context) # Asumiendo que esta es tu plantilla para la lista de libros

def listar_autores(request):
    autores = Autor.objects.all().order_by('nombre') # Obtener todos los autores
    context = {
        'autores': autores,
        'title': 'Lista de Autores'
    }
    return render(request, 'autores.html', context) # Necesitarás crear esta plantilla

def listar_editoriales(request):
    editoriales = Editorial.objects.all().order_by('nombre') # Obtener todas las editoriales
    context = {
        'editoriales': editoriales,
        'title': 'Lista de Editoriales'
    }
    return render(request, 'editoriales.html', context) # Necesitarás crear esta plantilla

def contacto(request):
    """
    Vista para la página de contacto.
    """
    context = {
        'title': 'Contacto',
    }
    
    return render(request, 'contacto.html', context)
