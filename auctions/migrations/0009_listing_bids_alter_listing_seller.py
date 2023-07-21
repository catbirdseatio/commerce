# Generated by Django 4.2.3 on 2023-07-19 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0008_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="bids",
            field=models.ManyToManyField(
                through="auctions.Bid", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]