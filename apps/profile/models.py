import requests
from django.conf import settings
from django.db import models

from apps.catalog.models import Product


class Profile(models.Model):
    """Профиль"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField("Имя", max_length=1000)
    email = models.EmailField("Email", unique=True, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, unique=True, null=True, blank=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", null=True, blank=True)
    # default="media/default_avatar.jpg", null=True, blank=True)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return self.full_name

    def get_avatar(self):
        """Получить аватар, если аватара нет, то берем дефолтный"""
        base_url = "http://127.0.0.1:8000"
        if self.avatar:
            str_url = f"{base_url}{self.avatar.url}"
            url = requests.head(str_url).status_code
        else:
            url = 404
        if url == 200:
            return {
                "src": self.avatar.url,
                "alt": self.avatar.name,
            }
        else:
            return {
                "src": "/media/default_avatar.png",
                "alt": "default_avatar",
            }

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Basket(models.Model):
    """Корзина"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} от {self.created}"

    @property
    def count(self):
        """Количество товара в корзине"""
        return BasketProduct.objects.filter(basket=self).count()

    @property
    def total_price(self):
        """Итоговая цена товаров в корзине"""
        products = list(
            BasketProduct.objects.filter(basket=self).values_list(
                "product__price",
                flat=True,
            ),
        )
        return sum(products)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class BasketProduct(models.Model):
    """Товары в корзине"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count_product = models.PositiveIntegerField("Количество в корзине")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)


class Order(models.Model):
    """Заказ"""

    class DeliveryType(models.TextChoices):
        """Тип доставки"""

        DEFAULT = "DEFAULT", "Обычная доставка"
        EXPRESS = "EXPRESS", "Экспресс доставка"

    class StatusOrder(models.TextChoices):
        """Статус заказа"""

        NEW = "NEW", "Новый"
        ACCEPT = "ACCEPT", "Принят"
        PAID = "PAID", "Оплачен"
        WORK = "WORK", "В работе"
        DONE = "DONE", "Доставлен"

    class PaymentType(models.TextChoices):
        """Тип оплаты"""

        ONLINE = "ONLINE", "Моя карта"
        SOMEONE = "SOMEONE", "Чужая карта"

    delivery_type = models.CharField(
        "Доставка",
        max_length=8,
        default=DeliveryType.DEFAULT,
        choices=DeliveryType.choices,
    )
    total_cost = models.FloatField("Итоговая сумма", default=0)
    status = models.CharField(
        "Статус заказа",
        max_length=8,
        choices=StatusOrder.choices,
        default=StatusOrder.NEW,
    )
    city = models.CharField("Город", max_length=100, null=True, blank=True)
    address = models.CharField("Адрес", max_length=300, null=True, blank=True)
    payment_type = models.CharField(
        "Тип оплаты",
        max_length=8,
        choices=PaymentType.choices,
        default=PaymentType.ONLINE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    @property
    def fullName(self):
        """Полное имя покупателя"""
        return Profile.objects.get(user=self.user).full_name

    @property
    def email(self):
        """email покупателя"""
        return Profile.objects.get(user=self.user).email

    @property
    def phone(self):
        """Телефон покупателя"""
        return Profile.objects.get(user=self.user).phone

    def get_products(self):
        """Список товаров в корзине"""
        products = list(OrderProduct.objects.filter(order=self))
        result = []
        for i in products:
            result.append(
                {
                    "id": i.product.id,
                    "category": i.product.category.id,
                    "price": i.product.price,
                    "count": i.product.count_product,
                    "date": i.product.created,
                    "title": i.product.name,
                    "description": i.product.short_description,
                    "freeDelivery": i.product.free_delivery,
                    "images": i.product.get_images(),
                    "tags": i.product.get_tags(),
                    "reviews": i.product.reviews_count,
                    "rating": i.product.rating,
                },
            )
        return result

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(models.Model):
    """Товары в заказе"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count_product = models.PositiveIntegerField("Количество в заказе")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """Платежная информация"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    number = models.CharField("Номер", max_length=16)
    name = models.CharField("Имя держателя", max_length=1000)
    month = models.CharField("Месяц", max_length=2)
    year = models.CharField("Год", max_length=4)
    code = models.CharField("Код", max_length=4)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Платежная карта"
        verbose_name_plural = "Платежные карты"
