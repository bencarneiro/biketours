# Generated by Django 4.1.5 on 2024-01-18 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0009_tourtype_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourtype",
            name="price_in_cents",
            field=models.BigIntegerField(default=0),
        ),
    ]