from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
import re
from django.db import models
from django.utils.timezone import now
from decimal import Decimal, InvalidOperation

def current_year():
    return now().year

class Autor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(
        null=True,           # Allows NULL values in the database
        blank=True,          # Allows the field to be left blank in forms
        verbose_name="Fecha de nacimiento"
    )
    fecha_fallecimiento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de fallecimiento (opcional)"
    )
    biografia = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Biografía"
    )
    foto = models.ImageField(
        upload_to='autores/', 
        null=True, 
        blank=True, 
        verbose_name="Foto del autor"
    )
    
    premios = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Premios recibidos"
    )

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']
        unique_together = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def get_edad(self):
        if self.fecha_nacimiento is None:
            return "Desconocida" 

        if self.fecha_fallecimiento:
            return self.fecha_fallecimiento.year - self.fecha_nacimiento.year
        else:
            today = date.today()
            age = today.year - self.fecha_nacimiento.year
            if (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
                age -= 1
            return age

    def get_absolute_url(self):
        return reverse('inicio:detalle_autor', kwargs={'pk': self.pk})
    
class Editorial(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la editorial",
        unique=True,
        help_text="Nombre completo de la editorial"
    )
    pais = models.CharField(
        max_length=50,
        verbose_name="País de origen",
        default="Desconocido",
        help_text="País donde tiene su sede principal"
    )
    logo = models.ImageField(
        upload_to='editoriales/logos/%Y/%m/%d/',
        verbose_name="Logo de la editorial",
        null=True,
        blank=True,
        help_text="Sube el logo de la editorial (máx. 2MB)"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        blank=True,
        null=True,
        help_text="Historia y detalles relevantes de la editorial"
    )
    sitio_web = models.URLField(
        verbose_name="Sitio web oficial",
        blank=True,
        null=True,
        help_text="URL completa (ej: https://www.penguinrandomhouse.com)"
    )
    fundacion = models.PositiveIntegerField(
    verbose_name="Año de fundación",
    blank=True,
    null=True,
    validators=[
        MinValueValidator(1000),
        MaxValueValidator(timezone.now().year)  # Sin lambda
    ],
    help_text="Año de creación de la editorial (ej: 2013)"
    )
    
    slug = models.SlugField(
    max_length=100,
    unique=True,
    blank=True,
    null=True,  
    help_text="URL amigable (se genera automáticamente)"
)
    activa = models.BooleanField(
        verbose_name="Activa",
        default=True,
        help_text="Indica si la editorial sigue operando"
    )
    fecha_creacion = models.DateTimeField(
        verbose_name="Fecha de creación",
        auto_now_add=True
    )
    fecha_actualizacion = models.DateTimeField(
        verbose_name="Fecha de actualización",
        auto_now=True
    )

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.pais})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            
            counter = 1
            while Editorial.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.nombre)}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs)

    def clean(self):
        
        if len(self.nombre) < 3:
            raise ValidationError({
                'nombre': "El nombre debe tener al menos 3 caracteres"
            })
            
        if self.logo:
            if self.logo.size > 2 * 1024 * 1024:
                raise ValidationError({
                    'logo': "El tamaño del logo no debe exceder 2MB"
                })
                
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
            ext = os.path.splitext(self.logo.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError({
                    'logo': "Formato de imagen no soportado. Use JPG, PNG, GIF o SVG"
                })

    def get_absolute_url(self):
        return reverse('inicio:detalle_editorial', kwargs={'slug': self.slug})

    @property
    def nombre_completo(self):
        return f"{self.nombre} ({self.pais})"

    @property
    def año_fundacion(self):
        return self.fundacion.year if self.fundacion else None

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return '/static/img/default-editorial.png'

class Libro(models.Model):    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título completo del libro"
    )
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name="libros",
        verbose_name="Autor"
    )
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Editorial",
        related_name="libros"
    )
    isbn = models.CharField(
        max_length=17,
        verbose_name="ISBN",
        blank=True,
        null=True,
        help_text="Formato: 978-3-16-148410-0 o 0-306-40615-2"
    )
    año_publicacion = models.PositiveIntegerField(
    verbose_name="Año de publicación",
    validators=[
        MinValueValidator(1000, message="El año debe ser mayor a 1000"),
        MaxValueValidator(timezone.now().year, message="El año no puede ser futuro")
    ],
    blank=True,
    null=True
)
    precio = models.DecimalField(
        verbose_name="Precio",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        default=Decimal('0.00')  # Valor por defecto explícito
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        blank=True,
        null=True,
        help_text="Sinopsis o resumen del libro"
    )
    fecha_registro = models.DateTimeField(
        verbose_name="Fecha de registro",
        auto_now_add=True
    )
    disponible = models.BooleanField(
        verbose_name="Disponible",
        default=True
    )
    portada = models.ImageField(
        verbose_name="Portada del libro",
        upload_to='portadas/',
        null=True,
        blank=True,
        help_text="Formato: JPG, PNG o WEBP. Tamaño recomendado: 500x800px",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])
        ]
    )
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['-año_publicacion', 'titulo']
        unique_together = ['titulo', 'autor']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['año_publicacion']),
            models.Index(fields=['isbn']),  # Nuevo índice
        ]

    def __str__(self):
        return f"{self.titulo} ({self.año_publicacion})"

    def clean(self):
        """Validaciones personalizadas"""
        if len(self.titulo.strip()) < 3:
            raise ValidationError("El título debe tener al menos 3 caracteres")
    
        current_year = timezone.now().year
        if self.año_publicacion and self.año_publicacion > current_year:
            raise ValidationError("El año de publicación no puede ser futuro")
        
        if self.isbn and not self.validar_isbn():
            raise ValidationError({
                'isbn': "Formato ISBN inválido. Use ISBN-10 (ej. 0-306-40615-2) o ISBN-13 (ej. 978-3-16-148410-0)"
            })
        
        try:
            precio = Decimal(str(self.precio))
            if precio <= Decimal('0.00'):
                raise ValidationError({'precio': 'El precio debe ser mayor a 0'})
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError({'precio': 'El precio debe ser un número válido'})
            
    

    def validar_isbn(self):
        """Valida ISBN-10 o ISBN-13 sin dependencias externas"""
        isbn = self.isbn
        isbn_limpio = re.sub(r'[-\s]', '', isbn)
        
        if len(isbn_limpio) == 10:
            if not re.match(r'^\d{9}[\dX]$', isbn_limpio, re.IGNORECASE):
                return False
            
            total = sum((10 - i) * (int(c) if c != 'X' else 10) 
                       for i, c in enumerate(isbn_limpio[:-1]))
            check = (11 - (total % 11)) % 11
            check_char = 'X' if check == 10 else str(check)
            
            return isbn_limpio[-1].upper() == check_char
        
        elif len(isbn_limpio) == 13:
            if not isbn_limpio.isdigit() or not isbn_limpio.startswith(('978', '979')):
                return False
            
            total = sum(int(c) * (1 if i % 2 == 0 else 3) 
                      for i, c in enumerate(isbn_limpio[:-1]))
            check = (10 - (total % 10)) % 10
            
            return int(isbn_limpio[-1]) == check
        
        return False
        
class Resena(models.Model):
    TIPO_CHOICES = [
        ('LIBRO', 'Libro'),
        ('AUTOR', 'Autor'),
        ('EDITORIAL', 'Editorial'),
        ('OTRO', 'Otro'),
    ]    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE, null=True, blank=True)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE, null=True, blank=True)
    editorial = models.ForeignKey('Editorial', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    calificacion = models.IntegerField()
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} por {self.usuario.username}"
    
class Page(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenido = models.TextField()
    excerpt = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo