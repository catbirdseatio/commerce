from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from auctions.forms import CustomUserCreationForm, CustomUserChangeForm
from auctions.models import Listing, Category


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["img_preview", "title", "slug"]
