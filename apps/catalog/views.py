import logging
from datetime import datetime
from math import ceil

from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.serializers import CategoriesSerializer
from apps.catalog.serializers import ProductCatalogSerializer
from apps.catalog.serializers import ProductDetailSerializer
from apps.catalog.serializers import ReviewSerializer
from apps.catalog.serializers import SalesSerializer
from apps.catalog.serializers import TagSerializer
from apps.catalog.services import create_review
from apps.catalog.services import filter_catalog
from apps.catalog.services import filter_products
from apps.catalog.services import filter_reviews_by_product
from apps.catalog.services import filter_sales
from apps.catalog.services import filter_tags
from apps.catalog.services import get_all_products
from apps.catalog.services import get_count_products
from apps.catalog.services import get_count_sales
from apps.catalog.services import get_ids_product_in_banners
from apps.catalog.services import get_product_by_id
from apps.catalog.utils import get_catalog_filter

log = logging.getLogger(__name__)


class CategoriesView(generics.ListAPIView):
    serializer_class = CategoriesSerializer
    queryset = filter_catalog(query_lookups={"parent": None}, order_by="id")


class CatalogView(APIView):
    def get(self, request):
        query_lookups, order_by = get_catalog_filter(request.GET)
        products = filter_products(query_lookups, order_by)

        page_number = int(request.GET.get("currentPage"))
        page_size = int(request.GET.get("limit"))
        last_page = ceil(get_count_products() / page_size)

        paginator = Paginator(products, page_size)
        data_serialized = ProductCatalogSerializer(
            paginator.page(page_number),
            many=True,
            context={"request": request},
        ).data

        res = {
            "items": data_serialized,
            "currentPage": page_number,
            "lastPage": last_page,
        }

        return Response(res)


class TagView(APIView):
    def get(self, request):
        category_id = request.GET.get("category")
        tags = filter_tags(category_id)
        serializer_reviews = TagSerializer(tags, many=True).data
        return Response(serializer_reviews)


class ProductView(generics.RetrieveAPIView):
    queryset = get_all_products()
    serializer_class = ProductDetailSerializer


class ProductReviewView(APIView):
    def post(self, request, id_product):
        product = get_product_by_id(id_product)
        log.debug(f"ProductReviewView: {id_product=} {product=}")
        if product:
            data_review = {
                "author": request.data.get("author"),
                "email": request.data.get("email"),
                "text": request.data.get("text"),
                "rate": request.data.get("rate"),
                "product": product,
            }
            log.debug(f"ProductReviewView: {data_review=}")
            create_review(data_review)
            log.debug("ProductReviewView: create_review was successful")
            reviews = filter_reviews_by_product(product)
            log.debug(f"ProductReviewView: {reviews=}")
            serializer_reviews = ReviewSerializer(reviews, many=True).data
            return Response(serializer_reviews)


class ProductPopularView(generics.ListAPIView):
    serializer_class = ProductCatalogSerializer

    def get_queryset(self):
        return sorted(get_all_products(), key=lambda t: t.reviews_count, reverse=True)


class SalesView(APIView):
    def get(self, request):
        sales = filter_sales({"date_from__lte": datetime.now(), "date_to__gte": datetime.now()})

        page_number = int(request.GET.get("currentPage"))
        page_size = 10
        last_page = ceil(get_count_sales() / page_size)

        paginator = Paginator(sales, page_size)
        data_serialized = SalesSerializer(
            paginator.page(page_number),
            many=True,
            context={"request": request},
        ).data
        res = {"items": data_serialized, "currentPage": page_number, "lastPage": last_page}
        return Response(res)


class BannersView(generics.ListAPIView):
    product_ids = get_ids_product_in_banners()
    queryset = filter_products({"id__in": product_ids})
    serializer_class = ProductCatalogSerializer


class LimitedView(generics.ListAPIView):
    serializer_class = ProductCatalogSerializer
    queryset = filter_products({"is_limited": True})
