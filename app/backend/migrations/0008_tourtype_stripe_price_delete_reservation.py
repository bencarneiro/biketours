# Generated by Django 4.1.5 on 2024-01-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0007_checkoutsession_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourtype",
            name="stripe_price",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.DeleteModel(
            name="Reservation",
        ),
    ]
