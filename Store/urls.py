from django.urls import path
from .views import store,cart,cheackout,updatecart

urlpatterns = [
    path('',store,name='store'),
    path('cart/',cart,name='cart'),
    path('cheackout/',cheackout,name='checkout'),
    path('update_item/',updatecart,name='update_item')
]