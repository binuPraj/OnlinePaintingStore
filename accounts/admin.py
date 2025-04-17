from django.contrib import admin

from django.utils.html import format_html
from django.contrib import admin
from .models import Profile,CustomerProfile
#CartItems,WishlistItem,OrderItem,

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified', 'profile_image']  # Customize as needed

admin.site.register(Profile, ProfileAdmin)

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'fname' ,'lname','email', 'contact', 'street','city', 'district']

admin.site.register(CustomerProfile,CustomerProfileAdmin)



# class CartItemsAdmin(admin.ModelAdmin):
#     list_display = ('user','product_img','product_name', 'product_qty')  # Display product name, user, and quantity

#     def product_name(self, obj):
#         return obj.product.name  
#     def user(self, obj):
#         return obj.cart.user.username 

#     def product_img(self,obj):
#         if obj.product.image:
#             return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.product.image.url)
#         return "No Image"

#     product_img.short_description = "Product Image"

#     product_name.short_description = 'Product Name'  
#     user.short_description = 'User'  
# admin.site.register(CartItems,CartItemsAdmin)

# class WishlistItemAdmin(admin.ModelAdmin):
#     list_display = ('user','product_img','product_name')

#     def product_name(self, obj):
#         return obj.product.name  
#     def user(self, obj):
#         return obj.wishlist.user.username 

#     def product_img(self,obj):
#         if obj.product.image:
#             return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.product.image.url)
#         return "No Image"

#     product_img.short_description = "Product Image"

#     product_name.short_description = 'Product Name'  # Label for the Product Name column
#     user.short_description = 'User'
# admin.site.register(WishlistItem,WishlistItemAdmin)
# class OrderItemsAdmin(admin.ModelAdmin):
#     list_display = ('username', 'contact','product_image', 'product_name', 'price', 'quantity')

#     def product_image(self, obj):
#         # Ensure that 'obj.product' exists and has an image
#         if obj.product and obj.product.image:
#             return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.product.image.url)
#         return "No Image"

#     def product_name(self, obj):
#         return obj.product.name
    
#     def username(self, obj):
#         return obj.order.user.username  # Accessing the related User's username

#     def contact(self, obj):
#         return obj.order.contact
    
#     username.short_description = 'Username'
#     contact.short_description = 'Contact Number'
#     product_name.short_description = 'Product Name'
#     product_image.short_description = 'Product Image'

# admin.site.register(OrderItem, OrderItemsAdmin)


