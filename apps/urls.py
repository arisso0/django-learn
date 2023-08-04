from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.catalog.views import BannersView
from apps.catalog.views import CatalogView
from apps.catalog.views import CategoriesView
from apps.catalog.views import LimitedView
from apps.catalog.views import ProductPopularView
from apps.catalog.views import ProductReviewView
from apps.catalog.views import ProductView
from apps.catalog.views import SalesView
from apps.catalog.views import TagView
from apps.profile.views import AvatarChange
from apps.profile.views import BasketView
from apps.profile.views import login_view
from apps.profile.views import OrderDetailView
from apps.profile.views import OrderView
from apps.profile.views import PasswordChange
from apps.profile.views import PaymentView
from apps.profile.views import ProfileView
from apps.profile.views import sign_up


urlpatterns = [
    # ---- auth ----
    path("sign-in/", login_view, name="login"),
    path("sign-up/", sign_up, name="register"),
    path("sign-out/", LogoutView.as_view(), name="logout"),
    # ---- catalog ----
    path("categories/", CategoriesView.as_view()),
    path("catalog/", CatalogView.as_view()),
    path("products/popular/", ProductPopularView.as_view()),
    path("products/limited/", LimitedView.as_view()),
    path("sales/", SalesView.as_view()),
    path("banners/", BannersView.as_view()),
    # ---- basket ----
    path("basket/", BasketView.as_view()),
    # ---- orders ----
    path("orders/", OrderView.as_view()),
    path("order/<id_order>/", OrderDetailView.as_view()),
    # ---- payment ----
    path("payment/<id_payment>/", PaymentView.as_view()),
    # ---- profile ----
    path("profile/", ProfileView.as_view()),
    path("profile/avatar/", AvatarChange.as_view()),
    path("profile/password/", PasswordChange.as_view()),
    # ---- tags ----
    path("tags/", TagView.as_view()),
    # ---- product ----
    path("product/<int:pk>/", ProductView.as_view()),
    path("product/<int:id_product>/reviews/", ProductReviewView.as_view()),
]
