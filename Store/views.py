from django.shortcuts import render
from django.db.models import F,Sum
from django.http import JsonResponse
import json
from .utils import cartData,cooikeCart,updateCookieCart
from .models import Order,Product,OrderItem,ShippingAddress
from CoreAuth.models import Customer


def store(request):
    products = Product.objects.all()
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'products':products,'items':items,'order':order}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'items':items,'order':order}
    return render(request,'store/cart.html',context)

def cheackout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'items':items,'order':order}
    context = {'items':items,'order':order}
    return render(request,'store/checkout.html',context)

from django.http import JsonResponse
from .models import Product
import json

def updatecart(request):
    if not request.user.is_authenticated:
        try:
            dataCookieCart =  updateCookieCart(request)
            product_quantity = dataCookieCart['product_quantity']
            total_product = dataCookieCart['total_product']
            cart_total = dataCookieCart['cart_total']
            cart_count = dataCookieCart['cart_count']
            deleted = dataCookieCart['deleted']
            cart = dataCookieCart['cart']
            
            response = JsonResponse({
                'message': 'Item updated',
                'newQuantity': product_quantity,
                'ProductTotal': total_product,
                'cartTotal': cart_total,
                'cartItemsCount': cart_count,
                'deleted': deleted,
            })
            
            response.set_cookie('cart', json.dumps(cart), max_age=3600 * 24 * 7)
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    if request.user.is_authenticated:
        datacart = json.loads(request.body)
        cart = cartData(request)
        
        product = Product.objects.get(id=datacart['productId'])
        customer = cart['customer']
        order = cart['order']
        print(order)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        deleted = False
        if datacart['action'] == 'add':
            orderItem.quantity = (orderItem.quantity + 1 ) 
        if datacart['action'] == 'remove':
            orderItem.quantity = (orderItem.quantity - 1 )  
        orderItem.save()        
        if datacart['action'] == 'delete':
            orderItem.delete()
            deleted = True
        if orderItem.quantity <= 0:
            orderItem.delete()
            deleted = True
    
    
        return JsonResponse({
        'message': 'Item updated',
        'newQuantity': 0 if deleted else orderItem.quantity,
        'ProductTotal': orderItem.total_price,
        'cartTotal': order.get_cart_total,
        'cartItemsCount': order.get_cart_items,
        'deleted':deleted
        })
    
   