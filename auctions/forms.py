from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from auctions.models import Listing, Bid, Comment


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
        fields = (
            "title",
            "description",
            "starting_bid",
            "profile_image",
            "category",
        )

    def clean_starting_bid(self):
        data = self.cleaned_data["starting_bid"]
        if data < 0.01:
            forms.ValidationError("Starting bid must be more than .01")
        return data


class BidForm(forms.ModelForm):
    form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        """Add user and listing to the form instance."""
        self.listing = kwargs.pop("listing")
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields = ("bid_price",)

    def clean_bid_price(self):
        data = self.cleaned_data.get("bid_price")
        if self.listing.number_of_bids > 0 and data <= self.listing.current_price:
            raise forms.ValidationError("Bid price must exceed current price")
        elif data < self.listing.current_price:
            raise forms.ValidationError(
                "Bid must be greater than or equal to starting bid"
            )

        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.listing = self.listing

        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    comment_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        """Add user and listing to the form instance."""
        self.listing = kwargs.pop("listing")
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ("content",)

    def clean_content(self):
        data = self.cleaned_data.get("content")
        if len(data) > 1000:
            raise forms.ValidationError("Content exceeds 1000 characters.")

        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.listing = self.listing

        if commit:
            instance.save()
        return instance
