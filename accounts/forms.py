from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Restaurant


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_restaurant_owner = forms.BooleanField(
        required=False,
        label='Register as Restaurant Owner'
    )
    is_inspector = forms.BooleanField(
        required=False,
        label='Register as Inspector'
    )
    is_customer = forms.BooleanField(
        required=False,
        label='Register as Customer',
        initial=True  # Default checked
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2',
                  'is_restaurant_owner', 'is_inspector', 'is_customer']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location']