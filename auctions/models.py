import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.db import models


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


class Category(models.Model):
    title = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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
        return mark_safe(f'<img src="{self.profile_image.url}" width="150" />')
    
    def __str__(self):
        return self.title