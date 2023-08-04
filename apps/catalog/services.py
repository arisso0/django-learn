import logging

from apps.catalog.models import Banner
from apps.catalog.models import Catalog
from apps.catalog.models import Product
from apps.catalog.models import Review
from apps.catalog.models import Sales
from apps.catalog.models import Tag

log = logging.getLogger(__name__)


def filter_catalog(query_lookups: dict, order_by: str = "created"):
    """Получить QuerySet товаров по заданному фильтру"""
    return Catalog.objects.filter(**query_lookups).order_by(order_by)


def filter_products(query_lookups: dict, order_by: str = "created"):
    """Получить QuerySet товаров по заданному фильтру"""
    return Product.objects.filter(**query_lookups).order_by(order_by)


def get_all_products():
    """Получить все товары"""
    return Product.objects.all()


def get_count_products() -> int:
    """Получить число товаров"""
    return Product.objects.count()


def get_product_by_id(product_id: int) -> Product | None:
    """Получить товар по ID"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as error:
        log.error(f"{error=}")
        product = None
    return product


def filter_tags(category_id: int | None):
    """Получить теги в категории (все теги, если категории нет)"""
    if category_id:
        data = Tag.objects.filter(category__id=category_id)
    else:
        data = Tag.objects.all()
    return data


def filter_reviews_by_product(product: Product):
    """Получить отзывы товара"""
    return Review.objects.filter(product=product)


def create_review(data: dict) -> None:
    """Создать отзыв"""
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


def filter_sales(query_lookups: dict):
    """Получить товары на распродаже"""
    return Sales.objects.filter(**query_lookups)


def get_ids_product_in_banners() -> list:
    """Получить список ID товаров в баннерах"""
    return list(Banner.objects.all().values_list("product__id", flat=True))
