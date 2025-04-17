from django.shortcuts import redirect, render
from accounts.models import CartItems, Cart, Products,Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse


import random

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


        #need to correct later
        # For individual product checkout (when "product_uid" and "quantity" are in the URL)
        elif 'product_uid' in request.GET and 'quantity' in request.GET:
            product_uid = request.GET.get('product_uid')
            quantity = request.GET.get('quantity')

            try:
                product = Products.objects.get(uid=product_uid)

                # Create a temporary cart item to pass to the template
                cart_item = CartItems(product=product, product_qty=quantity)

                return render(request, 'checkout/checkout.html', {
                    'cart_items': [cart_item]  # Pass it as a list for consistency
                })
            except Products.DoesNotExist:
                raise Http404("Product not found")
        
        else:
            raise Http404("Invalid checkout request")

    # Redirect to cart page for non-GET requests
    return redirect('cart')

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        try:
            # Check if payment_mode is provided
            payment_mode = request.POST.get('payment_mode')
            if not payment_mode:
                return JsonResponse({'status': 'error', 'message': 'Please select a payment method.'})

            neworder = Order(
                user=request.user,
                fname=request.POST.get('fname'),
                lname=request.POST.get('lname'),
                email=request.POST.get('email'),
                contact=request.POST.get('contact'),
                district=request.POST.get('district'),
                city=request.POST.get('city'),
                street=request.POST.get('street'),
                payment_mode=payment_mode,
                total_price=request.POST.get('total_price'),
            )

            # Generate tracking number...
            trackno = 'paint' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = 'paint' + str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackno
            neworder.save()

            # Process cart items...
            cart_items = CartItems.objects.filter(cart__user=request.user)
            for item in cart_items:
                if item.product.stock_quantity >= item.product_qty:
                    OrderItem.objects.create(
                        order=neworder,
                        product=item.product,
                        price=item.product.sell_price,
                        quantity=item.product_qty,
                    )
                    item.product.stock_quantity -= item.product_qty
                    item.product.save()
                    item.delete()

            return JsonResponse({'status': 'success', 'message': 'Order placed successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error has occured'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
