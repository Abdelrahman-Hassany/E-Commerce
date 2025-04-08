from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress
# Register your models here.

admin.site.site_header = "E-Commerce Administration"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "E-Commerce Admin Panel"


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
