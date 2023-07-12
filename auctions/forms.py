from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from auctions.models import Listing


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "starting_bid", "profile_image", "category",)
    
    def clean_starting_bid(self):
        data = self.cleaned_data["starting_bid"]
        if data < .01:
            forms.ValidationError("Starting bid must be more than .01")
        return data
    
