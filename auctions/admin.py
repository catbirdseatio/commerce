from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from auctions.forms import CustomUserCreationForm, CustomUserChangeForm
from auctions.models import Listing


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username"]

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['img_preview', 'title']
