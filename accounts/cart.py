
from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Products, CartItems, Cart, Wishlist,WishlistItem
from .wishlist import deletewishlistitem

def addtocart(request,skip_redirect=False):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_uid = request.POST.get('product_uid')
            try:
                product_check = Products.objects.get(uid=prod_uid)
            except Products.DoesNotExist:
                return JsonResponse({'status': "No such product found"})
            
            if CartItems.objects.filter(cart__user=request.user, product=product_check).exists():
                return JsonResponse({'status':'other','message': "Product already in Cart"})
            
            prod_qty = int(request.POST.get('product_qty'))
            if product_check.stock_quantity >= prod_qty:
                cart, created = Cart.objects.get_or_create(user=request.user) 
                CartItems.objects.create(cart=cart, product=product_check, product_qty=prod_qty)
                return JsonResponse({'status': 'success','message': f"{product_check.name} added to Cart"})
            elif product_check.stock_quantity==0:
                return JsonResponse({'status':'other','message': f"{product_check.name} is out of stock"})
            else:
                return JsonResponse({'status':'other','message': f"Only {product_check.stock_quantity} in stock"})
        else:
            return JsonResponse({'status': "Login to Continue"})
        
    # Skip redirect when skip_redirect=True
    if not skip_redirect:
        return redirect('/')
    
def cart_view(request):
    #get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None 

    if cart:
        # get all cartitems of that user
        cart_items = CartItems.objects.filter(cart=cart)
    else:
        cart_items = []

    context = {'cart': cart, 'cart_items': cart_items}
    return render(request, "base/cart.html", context)

def update_cart(request):
    if request.method == 'POST':
        prod_uid = request.POST.get('product_uid')
        
        try:
            
            cart_item = CartItems.objects.get(cart__user=request.user, product__uid=prod_uid)
            
            prod_qty = int(request.POST.get('product_qty'))
            cart_item.product_qty = prod_qty
            cart_item.save()
            
            return JsonResponse({'status': "Updated Successfully"})
        except CartItems.DoesNotExist:
            return JsonResponse({'status': "Item not found in the cart"}, status=404)

def deletecartitem(request):
    if request.method == 'POST':
        prod_uid = request.POST.get('product_uid')
        try:
             
            cart_item = CartItems.objects.get(cart__user=request.user, product__uid=prod_uid)
            cart_item.delete()
            
            return JsonResponse({'status': "Deleted Successfully"})
        except ObjectDoesNotExist:

            return JsonResponse({'status': "Item does not exist"}, status=404)
    return redirect('/')

#one at a time add to cart from
def addtocartr(request):
    if request.method == 'POST':
        prod_uid = request.POST.get('product_uid')
        if not prod_uid:
            return JsonResponse({'status': "Product UID is missing"}, status=400)
        
        request.POST = request.POST.copy() 
        request.POST['product_uid'] = prod_uid  
        
        addtocart_response = addtocart(request, skip_redirect=True)
        
        deletewishlistitem_response = deletewishlistitem(request)
        
        return JsonResponse({
            "addtocart_status": addtocart_response.content.decode(),
            "deletewishlist_status": deletewishlistitem_response.content.decode(),
            'status':"success","message":"Added to Cart",
        })
    else:
        return JsonResponse({'status': "Invalid request method"}, status=405)


#######################need to fix here if out of stock no add to cart function to be shown####################
#add to cart from wishlist
def addtocartfromwishlist(request):
    if request.method == 'POST':
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
            
            if not wishlist_items:
                return JsonResponse({'status': "Wishlist is empty"}, status=400)

            cart, created = Cart.objects.get_or_create(user=request.user)

            if created and cart.user != request.user:
                return JsonResponse({'status': "Unauthorized access to cart"}, status=403)
                
            out_of_stock = []  

            for wishlist_item in wishlist_items:
                product = wishlist_item.product  
                if product.stock_quantity <= 0:
                    out_of_stock.append(product.uid) 
                    continue  

                # Check if the product already exists in the cart
                if CartItems.objects.filter(cart=cart, product=product).exists():
                    wishlist_item.delete()
                    continue  
                
                product_qty = int(request.POST.get(f'product_qty_{product.uid}', 1))

                CartItems.objects.create(cart=cart, product=product, product_qty=product_qty)
                wishlist_item.delete()
           
            

            # if out_of_stock:
            #     return JsonResponse({'status': "other", 'message':"Out of stock products"}, status=400)
            return JsonResponse({'status':'success','message':"Added to cart"})

        except Wishlist.DoesNotExist:
            return JsonResponse({'status': "Wishlist not found"}, status=404)
        except Exception as e:
            return JsonResponse({'status': f"An error occurred: {str(e)}"}, status=500)
    return redirect('/')

