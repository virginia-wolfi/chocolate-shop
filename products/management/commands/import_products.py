import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, ProductCategory
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Import products from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        products_to_create = []  # Список для массовой загрузки

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=",", quotechar='"')
            try:
                with transaction.atomic():  # Открываем транзакцию
                    for row in reader:
                        category = ProductCategory.objects.get(
                            name=row["category_name"]
                        )
                        product = Product(
                            name=row["name"],
                            description=row["description"],
                            price=float(row["price"]),  # Проверка на число
                            image=row["image"],
                            ingredients=row["ingredients"],
                            category=category,
                            slug=slugify(row["name"]),
                        )
                        products_to_create.append(product)  # Добавляем в список

                Product.objects.bulk_create(products_to_create)

                self.stdout.write(self.style.SUCCESS("Products imported successfully!"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing products: {e}"))
