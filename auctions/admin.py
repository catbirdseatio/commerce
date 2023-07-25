from typing import Any
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

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
    list_display = ["title", "slug", "listings_count"]
    
    @admin.display(ordering="listings_count")
    def listings_count(self, category):
        return category.listings_count
    
    def get_queryset(self, request):
        queryset =  super().get_queryset(request).annotate(
            listings_count=Count('listings'))
        return queryset


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["img_preview", "title", "slug", "listing_category", "starting_bid"]
    ordering = ["slug"]
    list_select_related = ['category']
    list_per_page = 10
    
    def listing_category(self, listing):
        if listing.category:
            return listing.category.slug
        else:
            return "None"
    