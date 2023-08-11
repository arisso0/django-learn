import json
import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profile.models import Order
from apps.profile.serializers import BasketProductSerializer
from apps.profile.serializers import OrderSerializer
from apps.profile.serializers import PaymentSerialiser
from apps.profile.serializers import ProfileSerializer
from apps.profile.services import create_basket_to_user
from apps.profile.services import create_order
from apps.profile.services import create_order_product
from apps.profile.services import create_payment
from apps.profile.services import create_user_profile
from apps.profile.services import delete_basket
from apps.profile.services import filter_basket_products_from_user
from apps.profile.services import get_basket_from_user
from apps.profile.services import get_order_by_query
from apps.profile.services import get_profile_from_user
from apps.profile.services import get_user_from_username
from apps.profile.utils import add_product_to_basket
from apps.profile.utils import check_user_in_db
from apps.profile.utils import delete_product_from_basket
from apps.profile.utils import get_image_from_request

log = logging.getLogger(__name__)


# region AUTH


@api_view(["POST"])
def login_view(request):
    """Аутентификация (вход)"""
    auth_dict = json.loads(list(request.POST.dict().keys())[0])
    username = auth_dict.get("username")
    password = auth_dict.get("password")
    log.debug(f"login_view: {auth_dict=}")
    user = authenticate(request, username=username, password=password)
    if user:
        log.debug(f"login_view: {user=}; begin login")
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        log.debug("login_view: user not found => 400")
        return Response("user not found", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def sign_up(request):
    """Регистрация"""
    if request.method == "POST":
        auth_dict = json.loads(list(request.POST.dict().keys())[0])
        name = auth_dict.get("name")
        username = auth_dict.get("username")
        password = auth_dict.get("password")
        log.debug(f"sign_up: {auth_dict=}")

        if check_user_in_db(username):
            log.debug("sign_up: user in db => 400")
            return Response("user is already exists", status=status.HTTP_400_BAD_REQUEST)

        create_user_profile(username, password, name)
        log.debug("sign_up: create_user_profile")
        return Response(status=status.HTTP_200_OK)


# endregion

# region PROFILE


class ProfileView(APIView):
    """Профиль: отображение и редактирование данных"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Отображение профиля"""
        user = request.user
        profile = get_profile_from_user(user=user)
        log.debug(f"ProfileView GET: {profile=}")
        if profile:
            data_serialized = ProfileSerializer(profile).data
            return Response(data_serialized)
        else:
            return Response("profile not found", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Редактирование данных профиля"""
        user = request.user
        instance = get_profile_from_user(user=user)
        log.debug(f"ProfileView POST: profile={instance}")
        if instance:
            serializer = ProfileSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("profile not found", status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(APIView):
    """Смена пароля"""

    def post(self, request):
        user = get_user_from_username(username=request.user.username)
        new_password = request.data.get("password")
        log.debug(f"PasswordChange: {user=}; {new_password=}")

        if user and new_password:
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("user or password not found", status=status.HTTP_400_BAD_REQUEST)


class AvatarChange(APIView):
    """Смена аватара"""

    def post(self, request):
        profile = get_profile_from_user(request.user)
        log.debug(f"AvatarChange: {profile=}")
        if profile:
            image = get_image_from_request(request, profile.id)
            log.debug(f"AvatarChange: {image=}")
            profile.avatar = image
            profile.save()
            # data_serialized = ProfileSerializer(profile).data
            # return Response(data_serialized)    # todo check valid response
            return Response(profile.get_avatar())
        else:
            return Response("profile not found", status=status.HTTP_400_BAD_REQUEST)


# endregion

# region ORDER, CART


class BasketView(APIView):
    """Корзина"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Отображение корзины"""
        products = filter_basket_products_from_user(request.user)
        log.debug(f"BasketView GET: {request.user=} {products=}")
        serializer_data = BasketProductSerializer(products, many=True)
        return Response(serializer_data.data)

    def post(self, request):
        """Добавление товара в корзину"""
        basket = get_basket_from_user(request.user)
        log.debug(f"BasketView POST: {request.user=} {basket=}")
        if not basket:
            log.error(f"BasketView POST: basket for {request.user} not found. begin create")
            basket = create_basket_to_user(request.user)

        result = add_product_to_basket(
            self.request.data.get("id"),
            self.request.data.get("count"),
            basket,
        )

        if result:
            log.error(result)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            products = filter_basket_products_from_user(self.request.user)
            log.debug(f"BasketView POST: {products=}")
            serializer_data = BasketProductSerializer(products, many=True)
            return Response(serializer_data.data)

    def delete(self, request):
        """Удаление товара из корзины"""
        product_id = request.data.get("id")
        product_count = request.data.get("count")
        log.debug(f"BasketView DELETE: {product_id=} {product_count}")
        result = delete_product_from_basket(request.user, product_id, product_count)
        if result:
            log.error(result)

        products = filter_basket_products_from_user(request.user)
        serializer_data = BasketProductSerializer(products, many=True)
        return Response(serializer_data.data)


class OrderView(APIView):
    """Заказы"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Отображение заказов"""
        user = request.user
        order = get_order_by_query({"user": user, "status": Order.StatusOrder.NEW})
        log.debug(f"OrderView GET: {user=} {order=}")
        if order:
            result = OrderSerializer(order).data
            return Response(result)
        else:
            return Response("order not found", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Создание заказа"""
        log.debug(f"OrderView POST: {request.user=}")
        order = create_order(user=request.user)
        log.debug(f"OrderView POST: {order.id=}")
        return Response({"orderId": order.id})


class OrderDetailView(APIView):
    """Текущий заказ"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id_order):
        """Отображение текущего заказа"""
        order = get_order_by_query({"id": id_order})
        log.debug(f"OrderDetailView GET: {id_order=}; {order=}")
        if order:
            result = OrderSerializer(order).data
            return Response(result)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id_order):
        """Оформление заказа"""
        log.debug(f"OrderDetailView POST: {id_order=}; {request.data}")

        order = get_order_by_query({"id": id_order})

        log.debug(f"OrderDetailView POST: {order=}")

        if order:
            data = request.data
            order.delivery_type = (
                data.get("deliveryType").upper()
                if data.get("deliveryType")
                else Order.DeliveryType.DEFAULT
            )
            order.total_cost = data.get("basketCount").get("price")
            order.city = data.get("city")
            order.address = data.get("address")
            order.payment_type = (
                data.get("paymentType").upper()
                if data.get("paymentType")
                else Order.PaymentType.ONLINE
            )
            order.status = order.StatusOrder.ACCEPT
            order.save()

            products = data.get("basket")
            [create_order_product(order, pr, products[pr].get("count")) for pr in products]

            result = OrderSerializer(order).data

            return Response(result)
        else:
            return Response("order not found", status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    """Оплата заказа"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id_payment):
        log.debug(f"PaymentView: {request.data=}")

        payment_data = {
            "number": request.data.get("number"),
            "name": request.data.get("name"),
            "month": request.data.get("month"),
            "year": request.data.get("year"),
            "code": request.data.get("code"),
        }
        if all(payment_data.values()):
            payment_data.update({"order": get_order_by_query({"id": id_payment})})
            payment = create_payment(payment_data)

            log.debug(f"PaymentView: {payment_data=}; {payment=}")

            serializer_data = PaymentSerialiser(payment).data
            delete_basket(request.user)  # удаляем корзину

            return Response(serializer_data)
        else:
            return Response("one or more data not found", status=status.HTTP_400_BAD_REQUEST)


# endregion
