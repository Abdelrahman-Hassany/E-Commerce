from django.urls import path
from .views import store,cart,cheackout,updatecart,processOrder

urlpatterns = [
    path('',store,name='store'),
    path('cart/',cart,name='cart'),
    path('checkout/',cheackout,name='checkout'),
    path('update_item/',updatecart,name='update_item'),
    path('process_order/', processOrder,name='process_order'),
    path('confirmation/', processOrder,name='confirmation'),

]