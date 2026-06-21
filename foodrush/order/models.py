from django.db import models
from django.conf import settings
from hotels.models import FoodItem,Hotel


# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)

    def totalamount(self):
        return self.quantity * self.fooditem.price

class Orders(models.Model):
    status_choices = (
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('OUT FOR DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address=models.TextField()
    order_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100,blank=True, null=True)
    payment_id =models.CharField(max_length=100,blank=True,null=True)
    ordered_at=models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    status=models.CharField(choices=status_choices,default='pending',max_length=100)
    amount=models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='items')
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField()



