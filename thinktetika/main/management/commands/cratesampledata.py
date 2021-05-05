import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from main.models_factory import ProductFactory, TagFactory

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Создание рандомной модели Product для тестирования'

    def add_arguments(self, parser):
        parser.add_argument('random_product', nargs=1, type=str)

    def handle(self, *args, **options):
        try:
            product = ProductFactory.create(tags=(TagFactory(), TagFactory()))
            self.stdout.write(
                self.style.SUCCESS('product created: ' + product.title))
        except Exception as e:
            raise CommandError('error: ' + str(e))
