from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#class User import AbstractUser for add some fields for user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    
#Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,blank=True,null=True,on_delete=models.CASCADE,related_name='customer')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

#Seller Model  
class Seller(models.Model):
    class RatingChoice(models.IntegerChoices):
        NOT_RATED = 0, 'Not Rated Yet'
        VERY_POOR = 1, 'Very Poor'
        POOR = 2, 'Poor'
        AVERAGE = 3, 'Average'
        GOOD = 4, 'Good'
        EXCELLENT = 5, 'Excellent'
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,blank=True,null=True,on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    store_description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=RatingChoice.choices, default=RatingChoice.NOT_RATED)

    def __str__(self):
        return self.name