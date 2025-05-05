from django.core.management.base import BaseCommand
from app.models import Category

class Command(BaseCommand):
    help = 'Add core PC component categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            "CPU (Processor)",
            "Motherboard",
            "Memory (RAM)",
            "Internal Hard Drive (HDD)",
            "Solid State Drive (SSD)",
            "Graphics Card (GPU)",
            "Power Supply Unit (PSU)",
            "Computer Case (Cabinet)",
            "CPU Cooler",
            "Case Fans",
            "Thermal Paste",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Headphones / Headsets",
            "Speakers",
            "Operating Systems (OS)"
        ]

        for name in categories:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Added: {name}'))
            else:
                self.stdout.write(f'ℹ️ Already exists: {name}')