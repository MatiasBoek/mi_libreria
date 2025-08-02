from django.contrib import admin
from .models import Autor, Editorial, Libro, Resena, Page 

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editorial', 'año_publicacion', 'precio') 
    list_filter = ('autor', 'editorial')  
    search_fields = ('titulo', 'autor__nombre')  
    ordering = ('titulo',)  

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Resena)
admin.site.register(Page)

