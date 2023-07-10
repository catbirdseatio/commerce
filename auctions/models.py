from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


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
    category = models.ForeignKey(
        Category,
        related_name="listings",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title