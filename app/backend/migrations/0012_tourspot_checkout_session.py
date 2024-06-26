# Generated by Django 4.1.5 on 2024-01-19 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0011_checkoutsession_stripe_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourspot",
            name="checkout_session",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="backend.checkoutsession",
            ),
        ),
    ]
