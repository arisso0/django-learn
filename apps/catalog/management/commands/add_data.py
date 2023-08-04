import os

from django.core.cache import cache
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.catalog.models import Catalog
from diploma.settings import BASE_DIR

IMAGE_PATH = os.path.join(BASE_DIR, "apps", "catalog", "_media_for_new_data")


class Command(BaseCommand):
    """
    what tables will be updated?
    "tables": "all"
    "tables": "ServiceCategory"
    "tables": "ImagesService"
    "tables": "LegalInformation"
    "tables": "FavouriteMedicalSection"
    """

    help = "Заполняет базу данными " "Список таблиц: \n" "all | " "tags | "  # ...

    def add_arguments(self, parser):
        parser.add_argument(
            "tables",
            type=str,
            help="Указывает какие таблицы нужно создать",
        )

    def handle(self, *args, **kwargs):
        tables = kwargs["tables"]
        self.stdout.write(f"add_data : {tables=}")
        data_catalog = {
            "Компьютеры": {"parent": None, "image": "techik.jpg"},
            "Ноутбуки": {"parent": "Компьютеры", "image": "techik.jpg"},
            "Мыши": {"parent": "Компьютеры", "image": "techik.jpg"},
            "Клавиатуры": {"parent": "Компьютеры", "image": "techik.jpg"},
            "Красота": {"parent": None, "image": "techik.jpg"},
            "Фены": {"parent": "Красота", "image": "techik.jpg"},
            "Плойки": {"parent": "Красота", "image": "techik.jpg"},
            "Газовые плиты": {"parent": None, "image": "techik.jpg"},
        }
        for data in data_catalog:
            if data_catalog[data]["parent"]:
                parent_catalog = Catalog.objects.get(name=data_catalog[data]["parent"])
            else:
                parent_catalog = None

            obj, _ = Catalog.objects.update_or_create(
                name=data,
                defaults={"parent": parent_catalog},
            )
            image_temp = os.path.join(IMAGE_PATH, data_catalog[data]["image"])
            obj.image.save(
                data_catalog[data]["image"],
                File(open(image_temp, "rb")),
            )
            obj.save()

        # tag_names = ["В подарок", "Для учебы", "Женщине", "Мужчине ", "Ребенку"]

        cache.clear()
