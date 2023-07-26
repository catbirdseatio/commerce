from typing import Any
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django.db.models import Count

from auctions.forms import CustomUserCreationForm, CustomUserChangeForm
from auctions.models import Listing, Category, Bid, Comment


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

    def listings_count(self, category):
        url = (
            reverse("admin:auctions_listing_changelist")
            + "?"
            + urlencode({"category__id": str(category.pk)})
        )

        return format_html('<a href="{}">{}</a>', url, category.listings_count)

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).annotate(listings_count=Count("listings"))
        )
        return queryset


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        "img_preview",
        "title",
        "category",
        "current_price",
        "bids",
        "comments",
    ]
    ordering = ["slug"]
    list_select_related = ["category", "seller"]
    list_per_page = 10

    def bids(self, listing):
        url = (
            reverse("admin:auctions_bid_changelist")
            + "?"
            + urlencode({"listing__id": str(listing.pk)})
        )
        return format_html('<a href="{}">{}</a>', url, "Bids")

    def comments(self, listing):
        url = (
            reverse("admin:auctions_comment_changelist")
            + "?"
            + urlencode({"listing__id": str(listing.pk)})
        )
        return format_html('<a href="{}">{}</a>', url, "Comments")

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related("bids")
            .prefetch_related("comments")
        )
        return queryset


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ["user", "bid_price", "created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "created_at"]
