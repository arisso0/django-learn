from io import BytesIO

import requests
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image

from apps.catalog.services import filter_products
from apps.catalog.services import get_product_by_id
from apps.profile.services import create_basket_products
from apps.profile.services import get_all_username
from apps.profile.services import get_basket_product_from_query
from apps.profile.services import get_products_ids_from_basket_products


def check_user_in_db(username: str) -> bool:
    """
    Проверить есть ли такой юзернейм в БД
    :param username: юзернейм
    """
    if username in get_all_username():
        return True
    else:
        return False


def get_image_from_request(request: requests.Request, profile_id: int) -> ContentFile:
    """
    Получить картинку из request
    :param request: реквест из запроса
    :param profile_id: ID профиля
    """
    img_io = BytesIO()
    original_image = Image.open(request.data.get("avatar"))
    rgb_im = original_image.convert("RGB")
    rgb_im.save(img_io, format="JPEG", quality=100)
    img_content = ContentFile(img_io.getvalue(), f"{profile_id}_avatar.jpg")
    return img_content


def add_product_to_basket(product_id: int, product_count: int, basket) -> None | str:
    """
    Добавить товар в корзину
    :param product_id: ID товара
    :param product_count: количество товара
    :param basket: корзина (объект)
    """
    product = get_product_by_id(product_id)

    # проверка возможности добавления товара в корзину
    if product and product.count_product >= product_count:
        existing_products_ids = get_products_ids_from_basket_products({"basket": basket})
        existing_products_in_basket = filter_products({"id__in": existing_products_ids})

        if product in existing_products_in_basket:  # если товар с таким ID уже есть в корзине
            bp = get_basket_product_from_query({"basket": basket, "product__id": product_id})
            if bp:
                bp.count_product += product_count
                bp.save()
        else:
            create_basket_products(product, product_count, basket)

        product.count_product -= product_count
        product.save()
    else:
        return "there is no such count of products OR no such product"


def delete_product_from_basket(user: User, product_id: int, product_count: int) -> None | str:
    """
    Удалить товар из корзины
    :param user: полозователь
    :param product_id: ID товара
    :param product_count: количество товара
    """
    exist_bp = get_basket_product_from_query({"basket__user": user, "product__id": product_id})
    if exist_bp.count_product - product_count > 0:
        exist_bp.count_product -= product_count
        exist_bp.save()
    elif exist_bp.count_product - product_count == 0:
        exist_bp.delete()
    else:
        return "not enough products!"
