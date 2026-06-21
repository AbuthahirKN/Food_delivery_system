from django.db import models
from django.conf import settings
# Create your models here.
class Hotel(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='hotels')

    def __str__(self):
        return self.hotel_name

class FoodItem(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='food')
    food_name=models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='foods')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name

