# Generated by Django 4.2.3 on 2023-08-01 11:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0007_alter_basket_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="basket",
            name="count",
        ),
        migrations.RemoveField(
            model_name="basket",
            name="total_price",
        ),
    ]