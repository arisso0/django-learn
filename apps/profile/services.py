import logging

from django.contrib.auth.models import User

from apps.catalog.models import Product
from apps.profile.models import Basket
from apps.profile.models import BasketProduct
from apps.profile.models import Order
from apps.profile.models import OrderProduct
from apps.profile.models import Payment
from apps.profile.models import Profile

log = logging.getLogger(__name__)


def get_all_username() -> list:
    """Получить все юзернеймы пользователей"""
    return list(User.objects.all().values_list("username", flat=True))


def create_user_profile(username: str, password: str, name: str) -> None:
    """Создать юзера и его профиль"""
    user = User.objects.create_user(username=username, password=password)
    name = name if name else username
    Profile.objects.create(user=user, full_name=name)


def get_user_from_username(username: str) -> User | None:
    """Получить пользователя по юзернейму"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as error:
        log.error(f"{error=}")
        user = None
    return user


def get_profile_from_user(user: User) -> Profile | None:
    """Получить профиль юзера"""
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist as error:
        log.error(f"{error=}")
        profile = None
    return profile


def create_basket_to_user(user: User) -> Basket:
    """Создать корзину по юзеру"""
    return Basket.objects.create(user=user)


def get_basket_from_user(user: User) -> Basket | None:
    """Получить корзину по юзеру"""
    try:
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist as error:
        log.error(f"{error=}")
        basket = None
    return basket


def delete_basket(user: User) -> None:
    """Удалить корзину юзера"""
    try:
        Basket.objects.get(user=user).delete()
    except Basket.DoesNotExist as error:
        log.error(f"{error=}")


def create_basket_products(product: Product, product_count: int, basket: Basket) -> None:
    """Добавить связку ТОВАР-КОРЗИНА"""
    BasketProduct.objects.create(
        product=product,
        count_product=product_count,
        basket=basket,
    )


def filter_basket_products_from_user(user: User):
    """Получить QuerySet связок ТОВАР-КОРЗИНА по пользователю"""
    return BasketProduct.objects.filter(basket__user=user)


def get_basket_product_from_query(query_lookup: dict) -> BasketProduct:
    """Получить связку ТОВАР-КОРЗИНА по заданным параметрам"""
    try:
        bp = BasketProduct.objects.get(**query_lookup)
    except BasketProduct.DoesNotExist as error:
        log.error(f"{error=}")
        bp = None
    return bp


def get_products_ids_from_basket_products(query_lookup: dict) -> set:
    """Получить ID товаров"""
    return set(
        BasketProduct.objects.filter(**query_lookup).values_list(
            "product__id",
            flat=True,
        ),
    )


def create_order(user: User) -> Order:
    """Создать новый заказ для Юзера"""
    return Order.objects.create(user=user)


def get_order_by_query(query_lookup: dict) -> Order | None:
    """Получить заказ по фильтру"""
    try:
        order = Order.objects.get(**query_lookup)
    except Order.DoesNotExist as error:
        log.error(f"{error=}")
        order = None
    return order


def create_order_product(order: Order, prodict_id: int, prodict_count: int) -> None:
    """Создать связь КОРИЗНА-ЗАКАЗ"""
    OrderProduct.objects.create(
        product=Product.objects.get(id=prodict_id),
        order=order,
        count_product=prodict_count,
    )


def create_payment(payment_data: dict) -> Payment:
    """Создать оплату"""
    return Payment.objects.create(**payment_data)
