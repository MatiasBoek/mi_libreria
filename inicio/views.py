from django.shortcuts import render, redirect
from .models import Autor, Editorial, Libro
from .forms import AutorForm, EditorialForm, LibroForm, BusquedaForm

def inicio(request):
    return render(request, 'gestion_libros/inicio.html')

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
            return redirect('gestion_libros:lista_autores')  # Ajusta el nombre
    else:
        form = AutorForm()
    return render(request, 'gestion_libros/agregar_autor.html', {'form': form})