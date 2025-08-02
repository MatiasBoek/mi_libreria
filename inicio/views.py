from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Editorial, Libro, Resena, Page
from .forms import AutorForm, EditorialForm, LibroForm, BusquedaForm, ResenaForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Page


def inicio(request):
    return render(request, 'gestion_libros/index.html')

# LIBRO

def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio:listar_libros')  # Ajusta este nombre según tus URLs
    else:
        form = LibroForm()
    
    return render(request, 'gestion_libros/agregar_libro.html', {'form': form})

def listar_libros(request):
    libros = Libro.objects.all().order_by('titulo') 
    context = {
        'libros': libros,
        'title': 'Lista de Libros'
    }
    return render(request, 'gestion_libros/libros.html', context)

# In inicio/views.py

def detalle_libro(request, pk):
    """
    Vista para mostrar los detalles de un libro específico.
    """
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'gestion_libros/detalle_libro.html', {'libro': libro})

def editar_libro(request, pk):
    """
    Vista para editar un libro existente.
    """
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro se ha actualizado con éxito.')
            return redirect('inicio:detalle_libro', pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'gestion_libros/editar_libro.html', {
        'form': form,
        'libro': libro
    })

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
    return render(request, 'gestion_libros/autores.html', context) 

   
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
    return render(request, 'gestion_libros/editoriales.html', context) # Necesitarás crear esta plantilla

# CONTACTO
def contacto(request):
    """
    Vista para la página de contacto.
    """
    context = {
        'title': 'Contacto',
    }
    
    return render(request, 'gestion_libros/contacto.html', context)

# SOBRE MI
def sobre_mi(request):
    return render(request, 'gestion_libros/sobre_mi.html')

# BLOG

def listar_resenas(request):
    resenas = Resena.objects.all()
    return render(request, 'gestion_libros/resenas.html', {'resenas': resenas})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'gestion_libros/registro.html', {'form': form})

def perfil_usuario(request):
    return render(request, 'gestion_libros/perfil.html', {'user': request.user})

@login_required
def crear_resena(request):
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            resena.save()
            return redirect('inicio:listar_resenas')
    else:        
        form = ResenaForm()    
    
    return render(request, 'gestion_libros/crear_resena.html', {'form': form})

def detalle_resena(request, pk):
    resena = get_object_or_404(Resena, pk=pk)
    return render(request, 'gestion_libros/detalle_resena.html', {'resena': resena})

@login_required
def mis_resenas(request):
    resenas = Resena.objects.filter(usuario=request.user)
    return render(request, 'gestion_libros/mis_resenas.html', {'resenas': resenas})

def listar_paginas(request):
    paginas = Page.objects.all()
    return render(request, 'gestion_libros/listar_paginas.html', {'paginas': paginas})

def detalle_pagina(request, pk):
    pagina = get_object_or_404(Page, pk=pk)
    return render(request, 'gestion_libros/detalle_pagina.html', {'pagina': pagina})



