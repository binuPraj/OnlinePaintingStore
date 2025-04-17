from django.urls import path,include
from store import views,cart,wishlist,checkout

urlpatterns=[    
    path("",views.front,name='Painting Muse'), 
    #user urls
    path("home/",views.home,name='home'), 
    path("shop/", views.shop,name="shop"),
    path("product_search/",views.product_search,name="product_search"),
    path("shop/productdetail/<slug:slug>/", views.product_detail, name="product_detail"),
    path("shop/<slug:slug>/", views.product_category, name="product_category"),

    path("cart/",cart.cart_view,name="cart"),
    path('addtocart/', cart.addtocart , name="add_to_cart"),
    path('updatecart/',cart.update_cart,name="update_cart"),
    path('deletecartitem/',cart.deletecartitem,name="delete_cart_item"),
    
    path('addtowishlist/', wishlist.addtowishlist, name="add_to_wishlist"),
    path('checkwishlist/', wishlist.checkwishlist, name='checkwishlist'),
    path('updatewishlist/',wishlist.updatewishlist,name="update_wishlist"),
    path('wishlist/', wishlist.wishlist_view, name="wishlist"),
    path('deletewishlistitem/',wishlist.deletewishlistitem,name="delete_wishlist_item"),

    path('addtocartr/',cart.addtocartr, name="add_to_cartr"),
    path('addtocartfromwishlist/',cart.addtocartfromwishlist, name="add_to_cart_from_wishlist"),

    path('checkout/',checkout.checkout_view,name="checkout"),
    path('placeorder/',checkout.placeorder,name="placeorder"),
    # path('executepayment/',checkout.execute_payment, name='execute_payment'),
    
    path("billing/",checkout.billing,name="billing"),
    path("order_successcod/",checkout.order_successcod, name="ordersuccesscod"),          #cod success
    path('ordersuccess/', checkout.ordersuccess, name='ordersuccess'),        #paypal success

    path("orderfail/", checkout.orderfail, name="orderfail"),

    path('order/',checkout.order_view,name="order"),

    path('paypal/',include("paypal.standard.ipn.urls")),
    
]