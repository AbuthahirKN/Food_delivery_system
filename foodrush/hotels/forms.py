from django import forms
from hotels.models import Hotel,FoodItem

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food_name','description','price','image','available']


