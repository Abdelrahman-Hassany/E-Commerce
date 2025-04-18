from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress,OrderStatus
from CoreAuth.models import User,Customer,Seller
# Register your models here.
admin.site.site_header = "E-Commerce Administration"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "E-Commerce Admin Panel"

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(ShippingAddress)