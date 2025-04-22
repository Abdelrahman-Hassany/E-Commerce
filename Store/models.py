from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models import F


class Product(models.Model):
    class RatingChoice(models.IntegerChoices):
        NOT_RATED = 0, 'Not Rated Yet'
        VERY_POOR = 1, 'Very Poor'
        POOR = 2, 'Poor'
        AVERAGE = 3, 'Average'
        GOOD = 4, 'Good'
        EXCELLENT = 5, 'Excellent'
    slug = models.SlugField(max_length=160, unique=True,default='temp-slug')
    seller = models.ForeignKey('CoreAuth.Seller',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(choices=RatingChoice,default=RatingChoice.NOT_RATED)
    image = models.ImageField(upload_to='images/products', blank=True, null=True,max_length=255)
    digital = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            if self.image:
                url = self.image.url
                return url
        except:
            pass
        return '/static/images/placeholder.png'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class Order(models.Model):
    customer =  models.ForeignKey('CoreAuth.Customer',on_delete=models.SET_NULL,null=True,blank=True)
    seller = models.ForeignKey('CoreAuth.Seller',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200,null=True)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.annotate(product_price=F('quantity') * F('product__price'))
        total = sum(item.product_price for item in order_items)
        return total
    
    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())
        
    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True,)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name
    

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey('CoreAuth.Customer',on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
    
class OrderStatus(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETE = 'complete', 'Complete'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey('CoreAuth.Customer', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    seller = models.ForeignKey('CoreAuth.Seller', on_delete=models.CASCADE)
    statuschoice = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    date_updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return f"Order {self.order.id} - Product {self.product.name} - {self.statuschoice}"

    @property
    def is_complete(self):
        return self.statuschoice == self.StatusChoice.COMPLETE

    @property
    def is_pending(self):
        return self.statuschoice == self.StatusChoice.PENDING

class TrackShipment(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARED = 'prepared', 'Prepared'
        CANCELED = 'canceled' , 'Canceled'
    seller = models.ForeignKey('CoreAuth.Seller', on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey('CoreAuth.Customer', on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    shipmentstatus = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    orderstatus = models.ForeignKey(OrderStatus,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return f" Shipment id {str(self.id)} - Product Name {self.product.name} - Shipmentstatus {self.shipmentstatus}"