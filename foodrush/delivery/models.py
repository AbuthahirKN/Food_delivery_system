from django.db import models
from order.models import Orders
from django.conf import settings
# Create your models here.
class Delivery(models.Model):
    status_choices=(('ASSIGNED','Assigned'),
                    ('PICKED','Picked'),
                    ('NEAR DESTINATION','Near Destination'),
                    ('DELIVERED','delivered'))
    order=models.ForeignKey(Orders,on_delete=models.CASCADE)
    delivery_partner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    assign_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=status_choices,default='ASSIGNED',max_length=50)
    delivery_at=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.order.order_id


