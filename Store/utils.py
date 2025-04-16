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
    order = {'get_cart_total':0,'get_cart_item':0}
    cartItems = order['get_cart_item']
    print(cart)
    for i in cart:
        try:    
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            print('product',product) 
            total = (product.price * cart[i]['quantity'] )
            print('total',total) 

            order['get_cart_total'] += total
            print('order total',order['get_cart_total']) 
            order['get_cart_item'] = cartItems
            print('order item',order['get_cart_item'])
            item = {
                'id':product.id,
                'product':{
                'id':product.id,'name':product.name, 'price':product.price, 
                'imageURL':product.imageURL
                            }, 
                'quantity':cart[i]['quantity'],
                'digital':product.digital,'get_total':total,
                        }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except Exception as e:
            print(f"❌ Error in cookieCart for product ID {i}: {e}")
            
    return {'items': items,'order':order,'cartItems':cartItems,}
            

def cartData(request):
    
    if request.user.is_authenticated:
        if request.user.is_seller:
            customer = request.user.seller
            order, create = Order.objects.get_or_create(seller=customer,complete=False)
        if request.user.is_customer:
            customer = request.user.customer
            order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        data_cookie_cart = cooikeCart(request)
        customer = 'u need to login'
        order = data_cookie_cart['order']
        items = data_cookie_cart['items']

    return {'customer':customer,'order':order,'items':items}


