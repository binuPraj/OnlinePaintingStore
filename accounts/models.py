from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from store.models import Products

class Profile(BaseModel):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    profile_image=models.ImageField(upload_to='img/profile')

class CustomerProfile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=50, null=False)
    lname=models.CharField(max_length=50, null=False)
    email=models.CharField(max_length=50, null=False)
    contact=models.CharField(max_length=50, null=False)
    city=models.CharField(max_length=50, null=False)
    district=models.CharField(max_length=50, null=False)
    street=models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.user.username





# class Cart(BaseModel):
#     user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="carts")

# class CartItems(BaseModel):
#     cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
#     product=models.ForeignKey(Products, on_delete=models.CASCADE)
#     product_qty=models.IntegerField(null=False, blank=False)
#     created_at=models.DateTimeField(auto_now_add=True)
    


# class Wishlist(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")

# class WishlistItem(BaseModel):
#     wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

# class Order(BaseModel):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     fname=models.CharField(max_length=50,null=False)
#     lname=models.CharField(max_length=50,null=False)
#     email=models.CharField(max_length=50,null=False)
#     contact=models.CharField(max_length=15, null=False, blank=False)

#     district=models.CharField(max_length=50,null=False)
#     city=models.CharField(max_length=50,null=False)
#     street=models.CharField(max_length=50,null=False)
#     payment_mode=models.CharField(max_length=50,null=False)
#     total_price=models.FloatField(null=False, default=0)
#     orderstatus=(('Prending', 'Pending'),('Out For Delivery', 'Out For Delivery'),('Completed','Completed'))
#     status=models.CharField(max_length=150,choices=orderstatus, default='Pending')
#     message=models.TextField(null=True)
#     tracking_no=models.CharField(max_length=150,null=True,unique=True)

#     def __str__(self):
#         return '{} {}'.format(self.uid,self.tracking_no)
    
# class OrderItem(BaseModel):
#     order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_items')
#     product=models.ForeignKey(Products, on_delete=models.CASCADE)
#     price=models.FloatField(null=False)
#     quantity=models.IntegerField(null=False)

#     def __str__(self):
#         return '{} {}'.format(self.order.uid,self.order.tracking_no)



