from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Editorial, Libro, Resena, Page
from .forms import AutorForm, EditorialForm, LibroForm, BusquedaForm, ResenaForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.views.decorators.http import require_http_methods
from django.urls import reverse


# INDEX/INICIO

def inicio(request):
    return render(request, 'gestion_libros/index.html')

# LIBRO

@login_required
def agregar_libro(request):
    breadcrumbs = [
        {'name': 'Libros', 'url': reverse('inicio:listar_libros')},
        {'name': 'Agregar Libro', 'url': 'inicio:agregar_libro'}  
    ]
    
    autores = Autor.objects.all().order_by('apellido', 'nombre')
    editoriales = Editorial.objects.all().order_by('nombre')
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)  
        if form.is_valid():
            libro = form.save()
            messages.success(request, f'Libro "{libro.titulo}" agregado correctamente')
            return redirect('inicio:listar_libros')
    else:
        form = LibroForm()
    
    context = {
        'form': form,
        'autores': autores,
        'editoriales': editoriales,
        'breadcrumbs': breadcrumbs,
        'titulo': 'Agregar Nuevo Libro'
    }
    
    return render(request, 'gestion_libros/agregar_libro.html', context)

def listar_libros(request):
    libros = Libro.objects.all()
    
    context = {
        'libros': libros,
        'breadcrumbs': [
            {'name': 'Libros', 'url': reverse('inicio:listar_libros')}
        ]
    }
    return render(request, 'gestion_libros/libros.html', context)

# def detalle_libro(request, pk):
#     """
#     Vista para mostrar los detalles de un libro específico
#     """
#     libro = get_object_or_404(Libro, pk=pk)
    
#     context = {
#         'libro': libro,
#         'breadcrumbs': [
#             {'name': 'Libros', 'url': reverse('inicio:listar_libros')},
#             {'name': libro.titulo, 'url': ''}
#         ]
#     }
#     return render(request, 'gestion_libros/detalle_libro.html', context)

# @login_required
# def editar_libro(request, pk):
#     """
#     Vista para editar un libro existente
#     """
#     libro = get_object_or_404(Libro, pk=pk)
    
#     if request.method == 'POST':
#         form = LibroForm(request.POST, request.FILES, instance=libro)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'El libro se ha actualizado correctamente')
#             return redirect('inicio:detalle_libro', pk=libro.pk)
#     else:
#         form = LibroForm(instance=libro)
    
    # context = {
    #     'form': form,
    #     'libro': libro,
    #     'breadcrumbs': [
    #         {'name': 'Libros', 'url': reverse('inicio:listar_libros')},
    #         {'name': libro.titulo, 'url': reverse('inicio:detalle_libro', args=[libro.pk])},
    #         {'name': 'Editar', 'url': ''}
    #     ]
    # }
    # return render(request, 'gestion_libros/editar_libro.html', context)

# AUTOR

@login_required(login_url='inicio:login')  
def agregar_autor(request):
    breadcrumbs = [
        {'name': 'Autores', 'url': reverse('inicio:listar_autores')},
        {'name': 'Agregar Autor', 'url': reverse('inicio:agregar_autor')}
    ]
    
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Autor "{autor.nombre} {autor.apellido}" guardado con éxito.')
            return redirect('inicio:listar_autores')
    else: 
        form = AutorForm()
    
    context = {
        'form': form,
        'breadcrumbs': breadcrumbs,
        'titulo': 'Agregar Nuevo Autor'
    }
        
    return render(request, 'gestion_libros/agregar_autor.html', context)


def listar_autores(request):
    autores = Autor.objects.all().order_by('apellido', 'nombre')
    
    context = {
        'autores': autores,
        'title': 'Lista de Autores',
        'breadcrumbs': [ 
            {
                'name': 'Autores', 
                'url': reverse('inicio:listar_autores')
            }
        ]
    }
    return render(request, 'gestion_libros/autores.html', context)
   
def detalle_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    
    breadcrumbs = [
        {'name': 'Autores', 'url': reverse('inicio:listar_autores')},
        {'name': f"{autor.nombre} {autor.apellido}", 'url': ''},
    ]
    
    return render(request, 'gestion_libros/detalle_autor.html', {
        'autor': autor,
        'breadcrumbs': breadcrumbs
    })

@login_required
def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    form = AutorForm(instance=autor)
    
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            autor = form.save(commit=False)
            if 'foto' not in request.FILES and autor.foto:
                autor.foto = autor.foto
            autor.save()
            messages.success(request, 'Autor actualizado correctamente')
            return redirect('inicio:detalle_autor', pk=autor.pk)
    
    context = {
        'form': form,
        'autor': autor,
        'titulo': 'Editar Autor',
        'breadcrumbs': [
            {'name': 'Inicio', 'url': reverse('inicio:inicio')},
            {'name': 'Autores', 'url': reverse('inicio:listar_autores')},
            {'name': f'Editar {autor.nombre}', 'url': request.path}
        ]
    }
    return render(request, 'gestion_libros/editar_autor.html', context)

# BUSCAR

def buscar(request):
    resultados = None
    termino = ""
    
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
    
    breadcrumbs = [
        {'name': 'Buscar', 'url': reverse('inicio:buscar')}
    ]
    
    if termino:
        breadcrumbs.append(
            {'name': f'Resultados para "{termino}"', 'url': ''}
        )
    
    context = {
        'form': form,
        'resultados': resultados,
        'termino_busqueda': termino,
        'breadcrumbs': breadcrumbs
    }
    
    return render(request, 'gestion_libros/buscar.html', context)

#EDITORIAL

def listar_editoriales(request):
    editoriales = Editorial.objects.all().order_by('nombre')
    context = {
        'editoriales': editoriales,
        'title': 'Lista de Editoriales',
        'breadcrumbs': [
            {'name': 'Editoriales', 
             'url': reverse('inicio:listar_editoriales')}
        ]
    }
    return render(request, 'gestion_libros/editoriales.html', context)


@login_required
def agregar_editorial(request):
    # Configuración de breadcrumbs
    breadcrumbs = [
        {'name': 'Editoriales', 'url': reverse('inicio:listar_editoriales')},
        {'name': 'Agregar Editorial', 'url': ''}  # Último elemento sin enlace
    ]
    
    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            editorial = form.save()
            return redirect('inicio:listar_editoriales')
    else:
        form = EditorialForm()
    
    context = {
        'form': form,
        'breadcrumbs': breadcrumbs,
        'titulo': 'Agregar Nueva Editorial'
    }
    
    return render(request, 'gestion_libros/agregar_editorial.html', context)

def detalle_editorial(request, pk):
    """
    Vista para mostrar los detalles de una editorial específica
    """
    editorial = get_object_or_404(Editorial, pk=pk)
    context = {
        'editorial': editorial,
        'breadcrumbs': [
            {'name': 'Editoriales', 'url': reverse('inicio:listar_editoriales')},
            {'name': editorial.nombre, 'url': ''}
        ]
    }
    return render(request, 'gestion_libros/detalle_editorial.html', context)

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def editar_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    
    if request.method == 'POST':
        form = EditorialForm(request.POST, request.FILES, instance=editorial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editorial actualizada correctamente')
            return redirect('inicio:detalle_editorial', pk=editorial.pk)
    else:
        form = EditorialForm(instance=editorial)
    
    context = {
        'editorial': editorial,
        'form': form,
        'breadcrumbs': [
            {'name': 'Editoriales', 'url': reverse('inicio:listar_editoriales')},
            {'name': editorial.nombre, 'url': reverse('inicio:detalle_editorial', args=[editorial.pk])},
            {'name': 'Editar', 'url': ''}
        ]
    }
    return render(request, 'gestion_libros/editar_editorial.html', context)


# SOBRE MI
def sobre_mi(request):
    return render(request, 'gestion_libros/sobre_mi.html')

# CONTACTO

def contacto(request):
    context = {
        'title': 'Contacto',
        'breadcrumbs': [
            {'name': 'Contacto', 'url': reverse('inicio:contacto')}
        ]
    }
    return render(request, 'gestion_libros/contacto.html', context)


# BLOG

def listar_resenas(request):
    resenas = Resena.objects.all()
    return render(request, 'gestion_libros/resenas.html', {'resenas': resenas})


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
    pages = Page.objects.all()
    return render(request, 'pages/list.html', {'pages': pages})

def detalle_pagina(request, pk):
    page = get_object_or_404(Page, pk=pk)
    return render(request, 'pages/detail.html', {'page': page})

#AUTENTICACION

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'inicio:inicio')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'breadcrumbs': [
            {'name': 'Iniciar sesión', 'url': reverse('inicio:login')}
        ]
    }
    return render(request, 'gestion_libros/login.html', context)

def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio:inicio')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio:inicio')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'breadcrumbs': [
            {'name': 'Registro', 'url': reverse('inicio:registro')}
        ]
    }
    return render(request, 'gestion_libros/registro.html', context)

@require_http_methods(["GET", "POST"])
@login_required
def logout_view(request):
    logout(request)
    return redirect('inicio:logout_exito')

def logout_exito_view(request):
    return render(request, 'gestion_libros/logout.html')

def perfil_usuario(request):
    context = {
        'user': request.user,
        'breadcrumbs': [
            {'name': 'Perfil', 'url': reverse('inicio:perfil')}
        ]
    }
    return render(request, 'gestion_libros/perfil.html', context)

# TERMINOS Y CONDICIONES

def terminos_condiciones(request):
    context = {
        'breadcrumbs': [
            {'name': 'Términos y Condiciones', 'url': request.path}
        ]
    }
    return render(request, 'gestion_libros/terminos_condiciones.html', context)

#PRIVACIDAD

def politica_privacidad(request):
    context = {
        'breadcrumbs': [

            {'name': 'Privacidad', 'url': request.path}
        ]
    }
    return render(request, 'gestion_libros/privacidad.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def eliminar_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    
    if request.method == 'POST':
        nombre_editorial = editorial.nombre
        editorial.delete()
        messages.success(request, f'La editorial "{nombre_editorial}" ha sido eliminada correctamente')
        return redirect('inicio:listar_editoriales')
    
    # Si alguien intenta acceder por GET, redirigir a detalle
    return redirect('inicio:detalle_editorial', pk=pk)