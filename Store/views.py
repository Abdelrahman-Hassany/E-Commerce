from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
import math
from .utils import cartData, updateCookieCart, merge_cookie_cart_to_user_cart
from .models import (
    Order,
    Product,
    OrderItem,
    ShippingAddress,
    OrderStatus,
    TrackShipment,
)
from .forms import UploadProduct

# Handles upload product using form
@login_required
def upload_product_view(request):
    if request.method == "POST":
        form = UploadProduct(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_authenticated:
                if request.user.seller:
                    messages.success(request, "product uploaded Success!")
                    product.seller = request.user.seller
                    product.save()
                    return redirect("upload_product")
                elif request.user.customer:
                    messages.error(request, "You must be a seller to upload products!")
                    return redirect("upload_product")
    else:
        form = UploadProduct()
    context = {"form": form}
    return render(request, "store/upload.html", context)


def store(request):
    cart_cookie = json.loads(request.COOKIES.get("cart", "{}"))

    if (
        request.user.is_authenticated
        and cart_cookie
        and not request.session.get("cart_merged")
    ):
        merge_cookie_cart_to_user_cart(request)
        request.session["cart_merged"] = True
        context = cartData(request)
        response = redirect("cart")
        response.delete_cookie("cart")
        return response
    products = Product.objects.all()
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    context = {"products": products, "items": items, "order": order}
    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


def cheackout(request):
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    context = {"items": items, "order": order}
    return render(request, "store/checkout.html", context)


def updatecart(request):
    if not request.user.is_authenticated:
        try:
            dataCookieCart = updateCookieCart(request)
            product_quantity = dataCookieCart["product_quantity"]
            total_product = dataCookieCart["total_product"]
            cart_total = dataCookieCart["cart_total"]
            cart_count = dataCookieCart["cart_count"]
            deleted = dataCookieCart["deleted"]
            cart = dataCookieCart["cart"]

            response = JsonResponse(
                {
                    "message": "Item updated",
                    "newQuantity": product_quantity,
                    "ProductTotal": total_product,
                    "cartTotal": cart_total,
                    "cartItemsCount": cart_count,
                    "deleted": deleted,
                }
            )

            response.set_cookie("cart", json.dumps(cart), max_age=3600 * 24 * 7)
            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.user.is_authenticated:
        datacart = json.loads(request.body)
        cart = cartData(request)

        product = Product.objects.get(id=datacart["productId"])
        customer = cart["customer"]
        order = cart["order"]
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        deleted = False
        if datacart["action"] == "add":
            orderItem.quantity = orderItem.quantity + 1
        if datacart["action"] == "remove":
            orderItem.quantity = orderItem.quantity - 1
        orderItem.save()
        if datacart["action"] == "delete":
            orderItem.delete()
            deleted = True
        if orderItem.quantity <= 0:
            orderItem.delete()
            deleted = True

        return JsonResponse(
            {
                "message": "Item updated",
                "newQuantity": 0 if deleted else orderItem.quantity,
                "ProductTotal": orderItem.total_price,
                "cartTotal": order.get_cart_total,
                "cartItemsCount": order.get_cart_items,
                "deleted": deleted,
            }
        )


@login_required
def product_detail(request):
    try:
        if request.user.is_authenticated and request.user.seller:
            seller = request.user.seller
            order_status = OrderStatus.objects.filter(seller=seller)
            context = {"order_status": order_status}
            return render(request, "store/product_detail.html", context)
    except Exception as e:
        print(e)
        return redirect("store")


@login_required
def complete_order(request):
    data = json.loads(request.body)
    action = data.get("action")
    order_ids = data.get("order_ids", [])
    if action == "confirm_shipment":
        order_statuses = OrderStatus.objects.filter(id__in=order_ids)
        for item in order_statuses:
            shipments = item.trackshipment_set.all()
            for shipment in shipments:
                shipment.shipmentstatus = TrackShipment.StatusChoice.PREPARED
                shipment.save()
            item.statuschoice = OrderStatus.StatusChoice.COMPLETE
            item.save()
        return JsonResponse({"status": "completed", "updated_ids": order_ids})
    elif action == "cancel":
        order_statuses = OrderStatus.objects.filter(id__in=order_ids)

        for status in order_statuses:
            shipments = status.trackshipment_set.all()
            for shipment in shipments:
                shipment.shipmentstatus = TrackShipment.StatusChoice.CANCELED
                shipment.save()
            status.delete()

        return JsonResponse({"status": "cancelled"})
    return JsonResponse({"status": "no_action"})

@login_required
def trackShipment(request):
    track_shipment = TrackShipment.objects.none()  # default empty

    if request.user.is_seller:
        seller = request.user.seller
        track_shipment = TrackShipment.objects.filter(seller=seller)
    elif request.user.is_customer:
        customer = request.user.customer
        track_shipment = TrackShipment.objects.filter(customer=customer)

    context = {"track_shipment": track_shipment}
    return render(request, "store/trackshipment.html", context)

@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data["form"]["total"])

    customer = None
    seller = None
    order = None

    if request.user.is_seller:
        seller = request.user.seller
        order, create = Order.objects.get_or_create(seller=seller, complete=False)
    elif request.user.is_customer:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)

    if order is None:
        return JsonResponse({"message": "User not recognized."}, status=400)

    if math.isclose(total, order.get_cart_total, rel_tol=1e-9):
            order.complete = True
            
    order.transaction_id = transaction_id
    order.save()

    for order_item in order.orderitem_set.all():
        order_status_data = {
            "order": order,
            "product": order_item.product,
            "seller": order_item.product.seller,
            "address": data["form"]["address"],
            "quantity": order_item.quantity,
        }
        if customer:
            order_status_data["customer"] = customer

        order_status, create = OrderStatus.objects.get_or_create(**order_status_data)

        track_shipment_data = {
            "product": order_item.product,
            "quantity": order_item.quantity,
            "address": data["form"]["address"],
            "seller": order_item.product.seller,
            "orderstatus": order_status,
        }

        if customer:
            track_shipment_data["customer"] = customer

        TrackShipment.objects.get_or_create(**track_shipment_data)

    if customer:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["form"]["address"],
            city=data["form"]["city"],
            state=data["form"]["state"],
            zipcode=data["form"]["zipcode"],
        )

    messages.success(request, "Payment completed successfully!")
    return JsonResponse({"message": "Order completed successfully"}, status=200)