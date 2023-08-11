from rest_framework import serializers

from apps.catalog.models import Catalog
from apps.catalog.models import Product
from apps.catalog.models import Review
from apps.catalog.models import Sales
from apps.catalog.models import Tag


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для каталога: вывод категорий и подкатегорий для меню"""

    title = serializers.CharField(source="name")
    image = serializers.DictField(source="get_image")
    subcategories = serializers.ListField(source="get_subcategories")

    class Meta:
        model = Catalog
        fields = ["id", "title", "image", "subcategories"]
        depth = 3


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов: вывод тегов"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериалайзер для детального отображения товара (страница товара)"""

    count = serializers.IntegerField(source="count_product")
    date = serializers.CharField(source="created")
    title = serializers.CharField(source="name")
    description = serializers.CharField(source="short_description")
    fullDescription = serializers.CharField(source="full_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    images = serializers.ListField(source="get_images")
    tags = serializers.ListField(source="get_tags")
    reviews = serializers.ListField(source="get_reviews")
    specifications = serializers.ListField(source="get_specifications")

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]


class ProductCatalogSerializer(serializers.ModelSerializer):
    """Сериалайзер для товара: карточка товара на странице каталога"""

    count = serializers.IntegerField(source="count_product")
    category = serializers.PrimaryKeyRelatedField(source="category_id", read_only=True)
    date = serializers.CharField(source="created")
    title = serializers.CharField(source="name")
    description = serializers.CharField(source="short_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    images = serializers.ListField(source="get_images")
    tags = serializers.ListField(source="get_tags")
    reviews = serializers.IntegerField(source="reviews_count")

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов: вывод отзывов на странице товара"""

    date = serializers.CharField(source="created")

    class Meta:
        model = Review
        fields = [
            "author",
            "email",
            "text",
            "date",
            "rate",
        ]


class SalesSerializer(serializers.ModelSerializer):
    """Сериалайзер для раздела распродажи"""

    price = serializers.CharField(source="product.price")
    salePrice = serializers.CharField(source="sale_price")
    dateFrom = serializers.CharField(source="valid_date_from")
    dateTo = serializers.CharField(source="valid_date_to")
    title = serializers.CharField(source="product.name")
    images = serializers.ListField(source="product.get_images")

    class Meta:
        model = Sales
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
