from django.shortcuts import render
from django.db.models import F,Sum
from django.http import JsonResponse
import json
from .utils import cartData,cooikeCart
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
            data = json.loads(request.body)
            product_id = str(data['productId'])
            action = data['action']

            cart = json.loads(request.COOKIES.get('cart', '{}'))
            deleted = False

            if action == 'add':
                if product_id in cart:
                    cart[product_id]['quantity'] += 1
                else:
                    cart[product_id] = {'quantity': 1}

            elif action == 'remove':
                if product_id in cart:
                    cart[product_id]['quantity'] -= 1
                    if cart[product_id]['quantity'] <= 0:
                        del cart[product_id]
                        deleted = True

            elif action == 'delete':
                if product_id in cart:
                    del cart[product_id]
                    deleted = True

         
            cart_total = 0
            cart_count = 0
            for pid, details in cart.items():
                try:
                    product = Product.objects.get(id=pid)
                    cart_total += product.price * details['quantity']
                    cart_count += details['quantity']
                except Product.DoesNotExist:
                    continue

            response = JsonResponse({
                'message': 'Item updated',
                'deleted': deleted,
                'newQuantity': 0 if deleted else cart[product_id]['quantity'],
                'cartTotal': cart_total,
                'cartItemsCount': cart_count
            })
            response.set_cookie('cart', json.dumps(cart), max_age=3600 * 24 * 7)
            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        authenticated = True
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
    
    if authenticated:
        return JsonResponse({
        'message': 'Item updated',
        'newQuantity': 0 if deleted else orderItem.quantity,
        'cartItemsCount': order.get_cart_items,
        'deleted':deleted
        })
    
    if authenticated == False:
        return JsonResponse({'message':'u must log in'})