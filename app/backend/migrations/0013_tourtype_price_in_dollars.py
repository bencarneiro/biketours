# Generated by Django 4.1.5 on 2024-01-19 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0012_tourspot_checkout_session"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourtype",
            name="price_in_dollars",
            field=models.IntegerField(default=0),
        ),
    ]