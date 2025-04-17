from django.urls import path
from accounts import views
# ,cart,wishlist,checkout



urlpatterns=[    
    path('register/', views.register_view, name='register'),
    path("login/",views.login_view,name='login'), 
    path("logout/", views.logout_page, name='logout'),  # Logout confirmation page
    path("logout-confirm/", views.logout_confirm, name='logout_confirm'),  # Actual logout action
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),      #for account activation
    

    
    # path("cart/",cart.cart_view,name="cart"),
    # path('addtocart/', cart.addtocart , name="add_to_cart"),
    # path('updatecart/',cart.update_cart,name="update_cart"),
    # path('deletecartitem/',cart.deletecartitem,name="delete_cart_item"),
    
    # path('addtowishlist/', wishlist.addtowishlist, name="add_to_wishlist"),
    # path('checkwishlist/', wishlist.checkwishlist, name='checkwishlist'),
    # path('updatewishlist/',wishlist.updatewishlist,name="update_wishlist"),
    # path('wishlist/', wishlist.wishlist_view, name="wishlist"),
    # path('deletewishlistitem/',wishlist.deletewishlistitem,name="delete_wishlist_item"),

    # path('addtocartr/',cart.addtocartr, name="add_to_cartr"),
    # path('addtocartfromwishlist/',cart.addtocartfromwishlist, name="add_to_cart_from_wishlist"),

    # path('checkout/',checkout.checkout_view,name="checkout"),
    # path('placeorder/',checkout.placeorder,name="placeorder"),
]