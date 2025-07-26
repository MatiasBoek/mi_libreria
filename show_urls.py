from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Muestra todas las URLs registradas'

    def handle(self, *args, **options):
        resolver = get_resolver()
        for url_pattern in resolver.url_patterns:
            if hasattr(url_pattern, 'url_patterns'):
                # Para includes
                for pattern in url_pattern.url_patterns:
                    self.stdout.write(f"{pattern.pattern} -> {pattern.callback.__module__}.{pattern.callback.__name__}")
            else:
                self.stdout.write(f"{url_pattern.pattern} -> {url_pattern.callback.__module__}.{url_pattern.callback.__name__}")