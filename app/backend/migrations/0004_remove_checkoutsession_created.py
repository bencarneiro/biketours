# Generated by Django 4.1.5 on 2024-01-14 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_checkoutsession"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="checkoutsession",
            name="created",
        ),
    ]
