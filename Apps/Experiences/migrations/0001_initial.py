# Generated by Django 4.1.9 on 2023-08-12 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Technologies", "0001_initial"),
        ("Images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Experience",
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
                ("company", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
                ("description", models.TextField(max_length=1000)),
                ("url", models.CharField(blank=True, max_length=1000, null=True)),
                ("current", models.BooleanField(default=False)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "logo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Images.image",
                    ),
                ),
                (
                    "technologies",
                    models.ManyToManyField(
                        related_name="experiences", to="Technologies.technology"
                    ),
                ),
            ],
        ),
    ]
