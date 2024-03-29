# Generated by Django 4.1.7 on 2023-02-24 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Certifications", "0001_initial"),
        ("SocialNetworks", "0001_initial"),
        ("Images", "0001_initial"),
        ("Authors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("about", models.TextField(blank=True, max_length=5000)),
                ("cv", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to="Authors.author",
                    ),
                ),
                ("image", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="images",
                    to="Images.image"
                )),
            ],
        ),
    ]
