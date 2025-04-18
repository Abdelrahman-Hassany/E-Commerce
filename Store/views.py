from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import sweetify
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from .utils import cartData,cooikeCart,updateCookieCart,merge_cookie_cart_to_user_cart
from .models import Order,Product,OrderItem,ShippingAddress
from .forms import UploadProduct

@login_required
def upload_product_view(request):
    if request.method == 'POST':
        form = UploadProduct(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  
            if request.user.is_authenticated:
                if request.user.seller:
                    print('test')
                    messages.success(request, 'product uploaded Success!')
                    product.seller = request.user.seller
                    product.save()
                    return redirect('upload_product')
                elif request.user.customer:
                    print("User is a customer")
                    messages.error(request, 'You must be a seller to upload products!')
                    return redirect('upload_product')
        
    else:
        form = UploadProduct()
        
    context = {'form':form}
    return render(request,'store/upload.html',context)


def store(request):
    cart_cookie = json.loads(request.COOKIES.get('cart', '{}'))

    if request.user.is_authenticated and cart_cookie and not request.session.get('cart_merged'):
        merge_cookie_cart_to_user_cart(request)
        request.session['cart_merged'] = True
        context = cartData(request)
        response = redirect('cart')
        response.delete_cookie('cart')
        return response
    
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
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def cheackout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'items':items,'order':order}
    return render(request,'store/checkout.html',context)


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
    

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['form']['total'])

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        if total == order.get_cart_total:
            order.complete = True

        order.transaction_id = transaction_id
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['form']['address'],
            city=data['form']['city'],
            state=data['form']['state'],
            zipcode=data['form']['zipcode'],
        )

        return JsonResponse({'message': 'Order completed successfully'}, status=200)

    return JsonResponse({'message': 'You must log in'}, status=401)

def confirmation(request):
    return JsonResponse({'message':'payment succcess,thank u!'})
    
