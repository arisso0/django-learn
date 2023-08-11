import logging

from django.db.models import QuerySet

from apps.catalog.models import Banner
from apps.catalog.models import Catalog
from apps.catalog.models import Product
from apps.catalog.models import Review
from apps.catalog.models import Sales
from apps.catalog.models import Tag


log = logging.getLogger(__name__)


def filter_catalog(query_lookups: dict, order_by: str = "created") -> QuerySet:
    """
    Получить QuerySet категорий каталога по заданному фильтру
    :param query_lookups: набор фильтров для каталога
    :param order_by: значение, по которому будет сортировка, по умолчанию - "по созданию"
    """
    return Catalog.objects.filter(**query_lookups).order_by(order_by)


def filter_products(query_lookups: dict, order_by: str = "created") -> QuerySet:
    """
    Получить QuerySet товаров по заданному фильтру

    :param query_lookups: набор фильтров для каталога
    :param order_by: значение, по которому будет сортировка, по умолчанию - "по созданию"
    """
    return Product.objects.filter(**query_lookups).order_by(order_by)


def get_all_products() -> QuerySet:
    """Получить все товары"""
    return Product.objects.all()


def get_count_products() -> int:
    """Получить число товаров"""
    return Product.objects.count()


def get_product_by_id(product_id: int) -> Product | None:
    """
    Получить товар по ID
    :param product_id: ID товара
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as error:
        log.error(f"{error=}")
        product = None
    return product


def filter_tags(category_id: int | None) -> QuerySet:
    """
    Получить теги в категории (все теги, если категории нет)
    :param category_id: ID категории
    """
    if category_id:
        data = Tag.objects.filter(category__id=category_id)
    else:
        data = Tag.objects.all()
    return data


def filter_reviews_by_product(product: Product) -> QuerySet:
    """
    Получить отзывы товара
    :param product: товар (объект)
    """
    return Review.objects.filter(product=product)


def create_review(data: dict) -> None:
    """
    Создать отзыв
    :param data: данные для создания нового отзыва
    """
    Review.objects.create(
        author=data.get("author"),
        email=data.get("email"),
        text=data.get("text"),
        rate=data.get("rate"),
        product=data.get("product"),
    )


def get_count_sales() -> int:
    """Получить количество товаров на распродаже"""
    return Sales.objects.count()


def filter_sales(query_lookups: dict) -> QuerySet:
    """
    Получить товары на распродаже
    :param query_lookups: набор фильтров для каталога
    """
    return Sales.objects.filter(**query_lookups)


def get_ids_product_in_banners() -> list:
    """Получить список ID товаров в баннерах"""
    return list(Banner.objects.all().values_list("product__id", flat=True))
