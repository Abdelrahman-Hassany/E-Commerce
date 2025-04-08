from django.shortcuts import render
from .models import Product,Order,OrderItem,ShippingAddress
from django.db.models import F , Sum
from django.http import JsonResponse
import json
import datetime

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.annotate(product_price=F('quantity') * F('product__price'))
    else:
        items = []
        total_order = 0
        order = {'get_cart_total':0,'get_cart_item':0}
    
    products = Product.objects.all()
    context = {'products':products,'order':order}
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.annotate(product_price=F('quantity') * F('product__price'))
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0}
    context = {'items': items,
                'unit_price':[item.product_price for item in items],
                'order':order,
                }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.annotate(total_price=F('quantity') * F('product__price'))
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0}
    context = {'items': items,
                'order':order,
                'shipping':False,
                }
    return render(request,'store/checkout.html',context)

def updateitem(request):
    data = json.loads(request.body)
    ProductId = data['productID']
    action = data['action']

    print('product id:',ProductId)
    print('action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=ProductId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()
    return JsonResponse('item was add' , safe=False)

def processOrder(request):
    print('data:',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, creat = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
	            city=data['shipping']['city'],
	            state=data['shipping']['state'],
	            zipcode=data['shipping']['zipcode'],
            )

    else:
        print('user not loged')
    return JsonResponse('payment Submitted',safe=False)