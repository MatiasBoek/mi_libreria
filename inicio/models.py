from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Autor(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre completo",
        help_text="Nombre completo del autor",
        unique=True,
        error_messages={
            'unique': "Ya existe un autor con este nombre"
        }
    )
    nacionalidad = models.CharField(
        max_length=50,
        verbose_name="Nacionalidad",
        blank=True,
        null=True,
        default="Desconocida"
    )
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
        ]
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        if len(self.nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres")
        if self.nacionalidad and len(self.nacionalidad) < 3:
            raise ValidationError("La nacionalidad debe tener al menos 3 caracteres")

class Editorial(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la editorial",
        unique=True
    )
    pais = models.CharField(
        max_length=50,
        verbose_name="País de origen",
        default="Desconocido"
    )
    
    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.pais})"
    
    def clean(self):
        if len(self.nombre) < 3:
            raise ValidationError("El nombre de la editorial debe tener al menos 3 caracteres")

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
    año_publicacion = models.PositiveIntegerField(
        verbose_name="Año de publicación",
        validators=[
            MinValueValidator(1000, message="El año debe ser mayor a 1000"),
            MaxValueValidator(lambda: timezone.now().year, 
                            message="El año no puede ser futuro")
        ]
    )
    precio = models.DecimalField(
        verbose_name="Precio",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="El precio debe ser mayor a 0")]
    )
    fecha_registro = models.DateTimeField(
        verbose_name="Fecha de registro",
        auto_now_add=True
    )
    disponible = models.BooleanField(
        verbose_name="Disponible",
        default=True
    )
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['-año_publicacion', 'titulo']
        unique_together = ['titulo', 'autor']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['año_publicacion']),
        ]
    
    def __str__(self):
        return f"{self.titulo} ({self.año_publicacion})"
    
    def clean(self):
        if len(self.titulo) < 3:
            raise ValidationError("El título debe tener al menos 3 caracteres")
        
        # Validación personalizada adicional
        if self.año_publicacion and self.año_publicacion > timezone.now().year:
            raise ValidationError("El año de publicación no puede ser en el futuro")
        
        if self.precio and self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a cero")
