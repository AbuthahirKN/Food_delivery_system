from django import forms
from users.models import CustomUser,Review
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    class Meta:
         model= CustomUser
         fields=['username','email','password1','password2','phone','address','role']

    def __str__(self):
        return self.username


    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)

         for field in self.fields.values():
             field.help_text = None



class LoginForm(forms.Form):
    username= forms.CharField(max_length=40)
    password=forms.CharField(widget=forms.PasswordInput)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']


