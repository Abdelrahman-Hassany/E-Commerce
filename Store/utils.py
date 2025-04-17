from .models import Order,Product,OrderItem,ShippingAddress
from CoreAuth.models import Customer,Seller
from django.contrib.auth.decorators import login_required
import json

def cooikeCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
    for i in cart:
        try:    
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            print('product',product) 
            total = (product.price * cart[i]['quantity'] )
            print('total',total) 

            order['get_cart_total'] += total
            print('order total',order['get_cart_total']) 
            order['get_cart_items'] = cartItems
            print('order item',order['get_cart_items'])
            item = {
                'id':product.id,
                'product':{
                'id':product.id,'name':product.name, 'price':product.price, 
                'imageURL':product.imageURL
                            }, 
                'quantity':cart[i]['quantity'],
                'digital':product.digital,'total_price':total,
                        }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except Exception as e:
            print(f" Error in cookieCart for product ID {i}: {e}")
            
    return {'items': items,'order':order,'cartItems':cartItems,}
            
def cartData(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            customer = request.user.seller
        elif request.user.is_customer:
            customer = request.user.customer
     
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    else:
        data_cookie_cart = cooikeCart(request)
        customer = 'u need to login'
        order = data_cookie_cart['order']
        items = data_cookie_cart['items']

    return {'customer': customer, 'order': order, 'items': items}


def updateCookieCart(request):
    
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

    product = Product.objects.get(id=product_id)
    product_quantity = cart[product_id]['quantity'] if not deleted else 0
    
    total_product = product.price * product_quantity
    
    return {'product_quantity':product_quantity,
            'total_product':total_product,
            'cart_total':cart_total,
            'cart_count':cart_count,
            'deleted':deleted,
            'cart':cart}
    
    
def merge_cookie_cart_to_user_cart(request):
    cookie_cart = json.loads(request.COOKIES.get('cart', '{}'))
    
    if not cookie_cart:
        return

    if request.user.is_seller:
        customer = request.user.seller
        order, create = Order.objects.get_or_create(seller=customer, complete=False)
    elif request.user.is_customer:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        return

    for pid, details in cookie_cart.items():
        try:
            product = Product.objects.get(id=pid)
            quantity = details['quantity']
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += quantity
            order_item.save()
        except Product.DoesNotExist:
            continue

    
