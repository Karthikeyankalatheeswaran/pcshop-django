from django.core.management.base import BaseCommand
from app.models import Product, Category
import csv

class Command(BaseCommand):
    help = 'Import products from CSV files'

    def handle(self, *args, **kwargs):
        CSV_FILES = [
            "import_data/case-accessory.csv",
            "import_data/case-fan.csv",
            "import_data/case.csv",
            "import_data/cpu-cooler.csv",
            "import_data/cpu.csv",
            "import_data/external-hard-drive.csv",
            "import_data/fan-controller.csv",
            "import_data/headphones.csv",
            "import_data/internal-hard-drive.csv",
            "import_data/keyboard.csv",
            "import_data/memory.csv",
            "import_data/monitor.csv",
            "import_data/motherboard.csv",
            "import_data/mouse.csv",
            "import_data/optical-drive.csv",
            "import_data/os.csv",
            "import_data/power-supply.csv",
            "import_data/speakers.csv",
            "import_data/sound-card.csv",
            "import_data/thermal-paste.csv",
            "import_data/ups.csv",
            "import_data/video-card.csv",
            "import_data/webcam.csv",
            "import_data/wired-network-card.csv",
            "import_data/wireless-network-card.csv"
        ]

        for file_path in CSV_FILES:
            self.stdout.write(f"\n📥 Importing: {file_path}")
            try:
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                    if not rows:
                        self.stdout.write(self.style.WARNING(f"⚠️ Empty file: {file_path}"))
                        continue

                    self.stdout.write(self.style.NOTICE(f"🧾 Headers: {reader.fieldnames}"))
                    self.stdout.write(self.style.NOTICE(f"🔎 First row: {rows[0]}"))

                    for row in rows:
                        name = row.get("name", "").strip()
                        category_name = row.get("category", "").strip()

                        if not name or not category_name:
                            self.stdout.write(self.style.WARNING(f"⚠️ Skipped: {row}"))
                            continue

                        category, created = Category.objects.get_or_create(name=category_name)
                        product = Product(name=name, price=row.get("price", 0), category=category)
                        product.save()
                        self.stdout.write(self.style.SUCCESS(f"✅ Saved: {name}"))

            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"🚫 File not found: {file_path}"))