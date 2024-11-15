# Generated by Django 4.1.5 on 2024-11-10 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0014_confirmationemailsent"),
    ]

    operations = [
        migrations.CreateModel(
            name="Test",
            fields=[
                (
                    "id",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now=True)),
                ("passed", models.BooleanField(default=False)),
                ("log", models.TextField(null=True)),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="backend.test",
                    ),
                ),
            ],
        ),
    ]
