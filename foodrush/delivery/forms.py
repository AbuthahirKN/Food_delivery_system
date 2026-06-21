from django import forms
from delivery.models import Delivery
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields=['delivery_partner','status','delivery_at']

