import json
from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = 'Import products from data.json'

    def handle(self, *args, **kwargs):
        with open('data.json', 'r') as file:
            data = json.load(file)

        for item in data:
            name = item.get('name')
            price = item.get('price')
            description = item.get('description', '')
            image = item.get('image', '')

            if name and price is not None:
                try:
                    price = float(price)
                    Product.objects.get_or_create(
                        name=name,
                        defaults={'price': price, 'description': description, 'image': image}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added: {name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding {name}: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped item due to missing name or price'))