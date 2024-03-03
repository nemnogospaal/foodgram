import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.csv', nargs='?',
                            type=str)

    def handle(self, *args, **kwargs):
        with open(os.path.join(DATA_ROOT, kwargs['filename']),
                  encoding='utf-8') as ingredients_csv:
            reader = csv.DictReader(ingredients_csv)
            for ingredient in reader:
                Ingredient.objects.get_or_create(**ingredient)
