import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from products.models import ProductCategory


class Command(BaseCommand):
    help = "Import data from a CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        categories_to_create = []

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(
                file,
                quotechar='"',
                delimiter=",",
                quoting=csv.QUOTE_ALL,
                skipinitialspace=True,
            )
            with transaction.atomic():
                for row in reader:
                    category = ProductCategory(
                        name=row["name"],
                        description=row["description"],
                        slug=slugify(row["name"]),
                    )
                    categories_to_create.append(category)

                ProductCategory.objects.bulk_create(categories_to_create)
        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
