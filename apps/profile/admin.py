from django.contrib import admin

from .models import Basket
from .models import BasketProduct
from .models import Order
from .models import OrderProduct
from .models import Payment
from .models import Profile

admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(Basket)
admin.site.register(BasketProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
