# Generated by Django 4.1.6 on 2023-02-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Authors", "0001_initial"),
        ("Technologies", "0001_initial"),
        ("Images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(max_length=100)),
                ("introduction", models.CharField(max_length=500)),
                ("description", models.CharField(max_length=1000)),
                ("url", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "repository",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("authors", models.ManyToManyField(to="Authors.author")),
                ("images", models.ManyToManyField(blank=True, to="Images.image")),
                ("technologies", models.ManyToManyField(to="Technologies.technology")),
            ],
        ),
    ]
