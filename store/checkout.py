from django.shortcuts import redirect, render
from store.models import CartItems, Cart,Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
import random
from django.db.models import F
from accounts.models import Profile

import requests
import paypalrestsdk

#paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
import uuid #unique user id for duplicate orders

#for paypal payment
paypalrestsdk.configure({
    "mode": "sandbox",  
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


@login_required(login_url='login')
def checkout_view(request):
    if request.method == "GET":
        # For all cart items (when "all_items" is in the URL)
        if 'all_items' in request.GET:
            cart = Cart.objects.get(user=request.user)
            cart_items = []
            subtotal = 0
            for item in CartItems.objects.filter(cart=cart):
                #if item.is_in_stock():
                if item.product.stock_quantity != 0:
                    cart_items.append(item)
                    subtotal += item.product.sell_price * item.product_qty
                    
            tax_amount = round(subtotal * 0.13, 2)  # Calculate tax (rounded to 2 decimal places)
            total = round(subtotal + tax_amount, 2)
            context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total': total,
        }
            return render(request, 'base/checkout.html', context)

    return redirect('cart')

@csrf_protect
def placeorder(request):
    if request.method == "POST":
        payment_mode = request.POST.get('payment_mode')
        
        # Collect the order details from the POST data
        order_details = {
            'fname': request.POST.get('fname'),
            'lname': request.POST.get('lname'),
            'email': request.POST.get('email'),
            'contact': request.POST.get('contact'),
            'country': request.POST.get('country'),
            'city': request.POST.get('city'),
            'street': request.POST.get('street'),
            'total_price': request.POST.get('total_price'),
            'payment_mode': payment_mode,
        }

        request.session['order_details'] = order_details
        request.session.save() 

        if payment_mode == "paypal":
            return JsonResponse({"billing_page_url": "/billing/"})
        elif payment_mode == "COD":
            return JsonResponse({"success_page_url": "/order_successcod/"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required(login_url='login')
def billing(request):
    order_details = request.session.get('order_details')

    if not order_details:
        return redirect('/cart/')

    cart_items = CartItems.objects.filter(cart__user=request.user,product__stock_quantity__gt=0)
    paypal_form = None

    if request.method == "POST":
        total_price = order_details.get('total_price')
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_price,
            'item_name': 'Painting Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'http://{host}{reverse("ordersuccess")}',
            'cancel_url': f'http://{host}{reverse("orderfail")}',
            
        }

        # Create the PayPal form using PayPalPaymentsForm
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        print("PayPal Form Created:", paypal_form)

    print("paypal FORM PASSING")
    return render(request, 'billing.html', {
        'order_details': order_details,
        'paypal_form': paypal_form,
        'cart_items': cart_items,
    })

@login_required(login_url='login')
def ordersuccess(request):
    order_details = request.session.get('order_details')
    if not order_details:
        return redirect('/orderfail/')

    order_obj = order_details.copy()  
    order_obj['user'] = request.user
    print(order_obj)

    new_order = Order(**order_obj)

    trackno = 'paint' + str(random.randint(1111111, 9999999))
    while Order.objects.filter(tracking_no=trackno).exists():
        trackno = 'paint' + str(random.randint(1111111, 9999999))

    new_order.tracking_no = trackno
    new_order.payment_status= True
    new_order.save()

    cart_items = CartItems.objects.filter(cart__user=request.user)
    order_items = []  
    total_amount = 0  
    for item in cart_items:
        if item.product.stock_quantity >= item.product_qty:
            order_item = OrderItem.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.sell_price,
                quantity=item.product_qty,
            )
            order_items.append(order_item)  
            item.product.stock_quantity -= item.product_qty
            item.product.save()
            item.delete()

            total_amount += order_item.price * order_item.quantity
    total_amount+=0.13 * total_amount

    del request.session['order_details']
    context = {
        'order_items': order_items,
        'tracking_no': new_order.tracking_no,
        'total_amount': total_amount,
        'user': request.user,
        'order_details': order_obj,  
        'country': order_obj.get('country'),
        'city': order_obj.get('city'),
        'street': order_obj.get('street'),
    }
    return render(request, "base/ordersuccess.html", context)

@login_required(login_url='login')
def orderfail(request):
    return render(request,"base/orderfail.html")


def order_successcod(request):
    order_details = request.session.get('order_details')
    if not order_details:
        return redirect('/orderfail/')

    order_obj = order_details.copy()  
    order_obj['user'] = request.user
    print(order_obj)

    new_order = Order(**order_obj)

    trackno = 'paint' + str(random.randint(1111111, 9999999))
    while Order.objects.filter(tracking_no=trackno).exists():
        trackno = 'paint' + str(random.randint(1111111, 9999999))

    new_order.tracking_no = trackno
    new_order.payment_status= False
    new_order.save()

    cart_items = CartItems.objects.filter(cart__user=request.user)
    order_items = []  
    total_amount = 0  
    for item in cart_items:
        if item.product.stock_quantity >= item.product_qty:
            order_item = OrderItem.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.sell_price,
                quantity=item.product_qty,
            )
            order_items.append(order_item)  
            item.product.stock_quantity -= item.product_qty
            item.product.save()
            item.delete()

            total_amount += order_item.price * order_item.quantity
    total_amount+=0.13 * total_amount

    del request.session['order_details']
    context = {
        'order_items': order_items,
        'tracking_no': new_order.tracking_no,
        'total_amount': total_amount,
        'user': request.user,
        'order_details': order_obj,  
        'country': order_obj.get('country'),
        'city': order_obj.get('city'),
        'street': order_obj.get('street'),
    }
    return render(request, "base/ordersuccess.html", context)


@login_required(login_url='login')
def order_view(request):
    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request, "base/orders.html",context)