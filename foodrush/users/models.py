from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from hotels.models import Hotel
# Create your models here.
class CustomUser(AbstractUser):
    role_choices = (('CUSTOMER', 'Customer'), ('HOTELS', 'Hotels'), ('DELIVERY', 'Delivery'),('ADMIN','Admin'))
    role = models.CharField(choices=role_choices)
    phone=models.IntegerField(null=True)
    address=models.TextField(null=True)

class Review(models.Model):
    hotel= models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

