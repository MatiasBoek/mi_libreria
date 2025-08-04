from django import template

register = template.Library()

@register.inclusion_tag('breadcrumbs.html')
def show_breadcrumbs(request):
    path_parts = [p for p in request.path.split('/') if p]
    breadcrumbs = []
    url_accum = '/'
    
    # Mapeo manual para nombres e iconos (personaliza según tus URLs)
    name_map = {
        'pages': {'name': 'Páginas', 'icon': 'bi-file-text'},
        'libros': {'name': 'Libros', 'icon': 'bi-book'},
        # Añade más rutas según necesites
    }
    
    for part in path_parts:
        url_accum += f"{part}/"
        crumb_data = {
            'name': name_map.get(part, {}).get('name', part.replace('-', ' ').title()),
            'url': url_accum,
            'icon': name_map.get(part, {}).get('icon', '')
        }
        breadcrumbs.append(crumb_data)
    
    return {'breadcrumbs': breadcrumbs}