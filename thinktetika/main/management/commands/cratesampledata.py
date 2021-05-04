import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from main.models_factory import ProductFactory

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('random_product', nargs=1, type=str)

    def handle(self, *args, **options):
        ProductFactory()
        try:
            product = ProductFactory.create()
            self.stdout.write(
                self.style.SUCCESS('product created: ' + product.title))
        except Exception as e:
            logger.warning(format(e))
            raise CommandError('error: ' + str(e))
