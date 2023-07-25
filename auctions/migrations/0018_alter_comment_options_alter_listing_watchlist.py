# Generated by Django 4.2.3 on 2023-07-25 12:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0017_alter_listing_watchlist"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                editable=False,
                null=True,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
