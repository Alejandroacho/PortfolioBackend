# Generated by Django 4.1.6 on 2023-02-20 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("SocialNetworks", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("first_name", models.CharField(max_length=100, null=True)),
                ("last_name", models.CharField(max_length=100, null=True)),
                (
                    "social_networks",
                    models.ManyToManyField(
                        related_name="authors",
                        to="SocialNetworks.socialnetwork",
                    ),
                ),
            ],
        ),
    ]
