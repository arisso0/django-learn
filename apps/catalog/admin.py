from django.contrib import admin

from apps.catalog.models import Banner
from apps.catalog.models import Catalog
from apps.catalog.models import Image
from apps.catalog.models import Product
from apps.catalog.models import Review
from apps.catalog.models import Sales
from apps.catalog.models import Specification
from apps.catalog.models import SpecificationProduct
from apps.catalog.models import Tag

admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(Specification)
admin.site.register(SpecificationProduct)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Banner)
admin.site.register(Sales)
