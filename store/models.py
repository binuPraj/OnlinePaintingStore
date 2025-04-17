from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


#from filer.fields.image import FilerImageField

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Ensure slug is generated if it's not provided
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    
#product
class Products(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='img/pimg')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    artist = models.CharField(max_length=50, default='')
    size_in_length = models.IntegerField(null=True, blank=True)
    size_in_breadth = models.IntegerField(null=True, blank=True)
    description = HTMLField()
    original_price = models.IntegerField(validators=[MinValueValidator(50)], default=200)
    sell_price = models.IntegerField(validators=[MinValueValidator(50)], default=300)
    total_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stock_quantity = models.IntegerField(
        editable=False,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current quantity of the product available for sale (auto-updated)."
    )

    def save(self, *args, **kwargs):
        if self._state.adding:  # This checks if the instance is being created
            self.stock_quantity = self.total_quantity
        else:
            print(self.total_quantity)

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def clean(self):
        if self.sell_price < self.original_price:
            raise ValidationError("Sell price cannot be lower than the original price.")

    def __str__(self):
        return self.name

    @property
    def profit(self):
        return self.sell_price - self.original_price

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0


class Cart(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="carts")

class CartItems(BaseModel):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")

class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Order(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fname=models.CharField(max_length=50,null=False)
    lname=models.CharField(max_length=50,null=False)
    email=models.CharField(max_length=50,null=False)
    contact=models.CharField(max_length=15, null=False, blank=False)

    country=models.CharField(max_length=50,null=False)
    city=models.CharField(max_length=50,null=False)
    street=models.CharField(max_length=50,null=False)
    payment_mode=models.CharField(max_length=50,null=False)
    total_price=models.FloatField(null=False, default=0)
    orderstatus=(('Pending', 'Pending'),('Out For Delivery', 'Out For Delivery'),('Completed','Completed'))
    status=models.CharField(max_length=150,choices=orderstatus, default='Pending')
    payment_status=models.BooleanField(default=False)
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True,unique=True)

    def __str__(self):
        return '{} {}'.format(self.uid,self.tracking_no)
    
class OrderItem(BaseModel):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_items')
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.order.uid,self.order.tracking_no)


