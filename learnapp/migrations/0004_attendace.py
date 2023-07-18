# Generated by Django 4.1.5 on 2023-06-25 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learnapp", "0003_payments"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendace",
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
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("date", models.CharField(max_length=50)),
                ("logintime", models.CharField(max_length=50)),
                ("logouttime", models.CharField(max_length=50)),
                ("approved", models.BooleanField(default=False)),
            ],
        ),
    ]
