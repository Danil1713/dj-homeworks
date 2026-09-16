import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    help = 'Импорт телефонов из CSV'

    def handle(self, *args, **options):
        file_path = Path(settings.BASE_DIR) / 'phones.csv'

        with open(file_path, encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                Phone.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'price': Decimal(row['price']),
                        'image': row['image'],
                        'release_date': date.fromisoformat(
                            row['release_date']
                        ),
                        'lte_exists': row['lte_exists'] == 'True',
                        'slug': slugify(row['name']),
                    },
                )

        self.stdout.write(
            self.style.SUCCESS('Телефоны импортированы')
        )