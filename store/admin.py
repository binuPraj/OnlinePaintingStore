from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from django.contrib import admin
from .models import CartItems, Products,WishlistItem,Category,OrderItem
from django import forms


class CustomUserAdmin(DefaultUserAdmin):
    # Disable the "Add User" button in the admin panel
    def has_add_permission(self, request):
        return False

    # Optional: If you want to block adding users through URLs as well
    def add_view(self, request, form_url='', extra_context=None):
        return self.changelist_view(request)


admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)

class productadmin(admin.ModelAdmin):
    list_display=('display_image','name','category','artist','original_price','sell_price','total_quantity','stock_quantity')
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    display_image.short_description = "Image"
admin.site.register(Products,productadmin)

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('user','product_img','product_name', 'product_qty')  # Display product name, user, and quantity

    def product_name(self, obj):
        return obj.product.name  
    def user(self, obj):
        return obj.cart.user.username 

    def product_img(self,obj):
        if obj.product.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.product.image.url)
        return "No Image"

    product_img.short_description = "Product Image"

    product_name.short_description = 'Product Name'  
    user.short_description = 'User'  
admin.site.register(CartItems,CartItemsAdmin)

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user','product_img','product_name')

    def product_name(self, obj):
        return obj.product.name  
    def user(self, obj):
        return obj.wishlist.user.username 

    def product_img(self,obj):
        if obj.product.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.product.image.url)
        return "No Image"

    product_img.short_description = "Product Image"

    product_name.short_description = 'Product Name'  # Label for the Product Name column
    user.short_description = 'User'
admin.site.register(WishlistItem,WishlistItemAdmin)

class OrderItemForm(forms.ModelForm):
    payment_status = forms.BooleanField(initial=False, required=False)
    status = forms.CharField(max_length=100, required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def save(self, commit=True):
        order_item = super().save(commit=False)
        # Save to related Order model
        order_item.order.payment_status = self.cleaned_data.get('payment_status')
        order_item.order.status = self.cleaned_data.get('status')
        order_item.order.save()  # Save changes to the related Order model
        if commit:
            order_item.save()
        return order_item

class OrderItemsAdmin(admin.ModelAdmin):
    form = OrderItemForm
    list_display = ('product_name', 'quantity', 'price', 'payment_status', 'status', 
                    'tracking_no', 'username', 'contact', 'street', 'city', 'country')

    def product_name(self, obj):
        return obj.product.name if obj.product else "No Product"
    
    def payment_status(self, obj):
        return obj.order.payment_status if obj.order else "Not Set"

    def status(self, obj):
        return obj.order.status if obj.order else "Not Set"

    def tracking_no(self, obj):
        return obj.order.tracking_no if obj.order else "No Tracking Number"
    
    def username(self, obj):
        return obj.order.user.username if obj.order and obj.order.user else "No User"
    
    def contact(self, obj):
        return obj.order.contact if obj.order else "No Contact"
    
    def street(self, obj):
        return obj.order.street if obj.order else "No Street"

    def city(self, obj):
        return obj.order.city if obj.order else "No City"
    
    def country(self, obj):
        return obj.order.country if obj.order else "No Country"

    product_name.short_description = 'Product Name'
    payment_status.short_description = 'Payment Status'
    status.short_description = 'Order Status'
    tracking_no.short_description = 'Tracking Number'
    username.short_description = 'Username'
    contact.short_description = 'Contact Number'
    street.short_description = 'Street'
    city.short_description = 'City'
    country.short_description = 'Country'

admin.site.register(OrderItem, OrderItemsAdmin)