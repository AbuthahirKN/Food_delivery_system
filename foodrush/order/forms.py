from django import forms
from django.contrib.auth.forms import UserCreationForm
from order.models import Orders
class OrderForm(forms.ModelForm):
    payment_choices=(('COD','Cash On Delivery'),('ONLINE','Online'))
    payment_method=forms.ChoiceField(choices=payment_choices)
    class Meta:
        model = Orders
        fields = ['payment_method']

