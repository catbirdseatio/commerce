import uuid
import os
import string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.urls import reverse
from django.db import models
from django_extensions.db.fields import AutoSlugField


def path_and_rename(instance, filename):
    """Function to set a path and a uuid filename"""
    upload_to = "images"
    ext = filename.split(".")[-1]
    # set filename as random string
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class ListingManager(models.Manager):
    def get_active(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="bids"
    )
    bid_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ["bid_price"]

    def __str__(self):
        return f"Bid #{self.pk}: {self.bid_price}"


class Category(models.Model):
    title = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from="title")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})


class Listing(models.Model):
    title = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from="title")
    description = models.TextField()
    seller = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="+"
    )
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    profile_image = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        related_name="listings",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many To Many Fields
    watchlist = models.ManyToManyField(
        "User", related_name="watchlist", blank=True, null=True, editable=False
    )

    # Managers
    objects = ListingManager()
    
    class Meta:
        ordering = ["-created_at"]

    def img_preview(self):
        if self.profile_image:
            return mark_safe(f'<img src="{self.profile_image.url}" width="150" />')
        return None

    def slugify_function(self, content):
        return content.translate({ord(c): "-" for c in string.whitespace}).lower()

    def bid_queryset(self):
        return self.bids.filter(listing_id=self.pk)

    @property
    def number_of_bids(self):
        return self.bid_queryset().count()

    @property
    def high_bid(self):
        try:
            return self.bid_queryset().select_related("user").latest()
        except Bid.DoesNotExist:
            return None

    @property
    def current_price(self):
        try:
            return self.bids.latest().bid_price
        except Bid.DoesNotExist:
            return self.starting_bid

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if len(self.content) > 15:
            return f"{self.content[:15]}..."
        return self.content

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.listing.slug})
