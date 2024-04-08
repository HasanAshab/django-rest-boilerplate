from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string

class Command(BaseCommand):
    help = "Seed a model with it's factory"

    def add_arguments(self, parser):
        parser.add_argument('factory', type=str)
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        path = options.get('factory')
        count = options.get('count')
        factory = import_string(path)
        factory.create_batch(count)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded "{factory._meta.model.__name__}" with {count} records')
        )