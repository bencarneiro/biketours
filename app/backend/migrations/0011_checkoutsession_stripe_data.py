# Generated by Django 4.1.5 on 2024-01-18 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0010_tourtype_price_in_cents"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkoutsession",
            name="stripe_data",
            field=models.JSONField(blank=True, null=True),
        ),
    ]