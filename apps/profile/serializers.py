from rest_framework import serializers

from apps.profile.models import BasketProduct
from apps.profile.models import Order
from apps.profile.models import Payment
from apps.profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name")
    avatar = serializers.DictField(source="get_avatar", read_only=True)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        return instance

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class PaymentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]


class OrderSerializer(serializers.ModelSerializer):
    orderId = serializers.IntegerField(source="id")
    createdAt = serializers.DateTimeField(source="created")
    deliveryType = serializers.CharField(source="delivery_type")
    paymentType = serializers.CharField(source="payment_type")
    totalCost = serializers.FloatField(source="total_cost")
    products = serializers.ListField(source="get_products")

    class Meta:
        model = Order
        fields = [
            "id",
            "orderId",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]


class BasketProductSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source="count_product")
    id = serializers.IntegerField(source="product.id")
    category = serializers.PrimaryKeyRelatedField(source="product.category_id", read_only=True)
    price = serializers.CharField(source="product.price")
    date = serializers.CharField(source="product.created")
    title = serializers.CharField(source="product.name")
    description = serializers.CharField(source="product.short_description")
    freeDelivery = serializers.BooleanField(source="product.free_delivery")
    images = serializers.ListField(source="product.get_images")
    tags = serializers.ListField(source="product.get_tags")
    reviews = serializers.IntegerField(source="product.reviews_count")
    rating = serializers.CharField(source="product.rating")

    class Meta:
        model = BasketProduct
        fields = [
            # "orderId",
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
