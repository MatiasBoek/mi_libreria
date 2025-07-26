# Sistema de Gestión de Librería

Aplicación web Django que implementa el patrón MVT para gestionar libros, autores y editoriales.

## 🛠 Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install django`
5. Migrar la base de datos: 
   ```bash
   python manage.py makemigrations
   python manage.py migrate