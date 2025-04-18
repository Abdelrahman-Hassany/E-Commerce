from django.urls import path
from .views import store,cart,cheackout,updatecart,processOrder,confirmation,upload_product_view,product_detail

urlpatterns = [
    path('',store,name='store'),
    path('upload_product/',upload_product_view,name='upload_product'),
    path('cart/',cart,name='cart'),
    path('checkout/',cheackout,name='checkout'),
    path('update_item/',updatecart,name='update_item'),
    path('process_order/', processOrder,name='process_order'),
    path('confirmation/', confirmation,name='confirmation'),
    path('product_detail/', product_detail,name='product_detail'),


]