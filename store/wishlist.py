from django.shortcuts import redirect, render
from django.http import JsonResponse
from store.models import Products,Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from .cart import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_uid = request.POST.get('product_uid')
            try:
                product_check = Products.objects.get(uid=prod_uid)
            except Products.DoesNotExist:
                return JsonResponse({'status': "No such product found"})
            
            if WishlistItem.objects.filter(wishlist__user=request.user, product=product_check).exists():
                return JsonResponse({'status': "Product already in Wishlist"})
            
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)   
            WishlistItem.objects.create(wishlist=wishlist, product=product_check)
            return JsonResponse({'status': "Added to Wishlist"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')

@login_required(login_url='login')
def updatewishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_uid = request.POST.get('product_uid')

            try:
                product_check = Products.objects.get(uid=prod_uid)
            except Products.DoesNotExist:
                return JsonResponse({'status': "No such product found"}, status=404)

            wishlist_item = WishlistItem.objects.filter(wishlist__user=request.user, product=product_check).first()

            if wishlist_item:
                # Remove product from wishlist
                wishlist_item.delete()
                return JsonResponse({'status': "removed", 'message': "Removed from Wishlist", 'in_wishlist': False})

            else:
                # Add product to wishlist
                wishlist, created = Wishlist.objects.get_or_create(user=request.user)
                WishlistItem.objects.create(wishlist=wishlist, product=product_check)
                return JsonResponse({'status': "added", 'message': "Added to Wishlist", 'in_wishlist': True})

        else:
            return JsonResponse({'status': "Login to Continue"}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def checkwishlist(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            prod_uid = request.GET.get('product_uid')

            try:
                product_check = Products.objects.get(uid=prod_uid)
            except Products.DoesNotExist:
                return JsonResponse({'status': "No such product found"}, status=404)

            in_wishlist = WishlistItem.objects.filter(wishlist__user=request.user, product=product_check).exists()

            return JsonResponse({'in_wishlist': in_wishlist})

        else:
            return JsonResponse({'status': "Login to Continue"}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def wishlist_view(request):
    #get user's wishlist
    try:
        wish= Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wish = None 

    if wish:
    #get all wishlistitems of that user
        wishlist_items = WishlistItem.objects.filter(wishlist=wish)
    else:
        wishlist_items = []

    context = {'wish': wish, 'wishlist_items': wishlist_items}
    return render(request, "base/wishlist.html", context)

@login_required(login_url='login')
def deletewishlistitem(request):
    if request.method == 'POST':
        prod_uid = request.POST.get('product_uid')
        try:
             
            wishlist_item =WishlistItem.objects.get(wishlist__user=request.user, product__uid=prod_uid)
            wishlist_item.delete()
            
            return JsonResponse({'status': "Deleted Successfully"})
        except ObjectDoesNotExist:

            return JsonResponse({'status': "Item does not exist"}, status=404)
    return redirect('/')


        


     
