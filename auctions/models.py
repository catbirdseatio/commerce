from typing import Set
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


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = ["bid_price"]

    def __str__(self):
        return f"Bid #{self.pk}: {self.bid_price}"


class Category(models.Model):
    title = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Listing(models.Model): 
    title = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField()
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="+")
    bids = models.ManyToManyField(get_user_model(), through="Bid")
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def img_preview(self):
        if self.profile_image:
            return mark_safe(f'<img src="{self.profile_image.url}" width="150" />')
        return None
    
    def slugify_function(self, content):
        return content.translate({ord(c): '-' for c in string.whitespace}).lower()

    @property
    def number_of_bids(self):
        return (
            Bid.objects.prefetch_related("listing").filter(listing_id=self.pk).count()
        )
    
    @property
    def current_price(self):
        bids = Bid.objects.prefetch_related("listing").filter(listing_id=self.pk)

        if bids.count() > 0:
            return bids.latest().bid_price
        
        else:
            return self.starting_bid

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})
    
