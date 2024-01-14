# Generated by Django 4.1.5 on 2024-01-14 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0004_remove_checkoutsession_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkoutsession",
            name="created",
            field=models.DateTimeField(default="2024-01-01"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="checkoutsession",
            name="id",
            field=models.CharField(max_length=512, primary_key=True, serialize=False),
        ),
    ]
