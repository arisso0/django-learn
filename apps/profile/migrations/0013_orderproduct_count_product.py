# Generated by Django 4.2.3 on 2023-08-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0012_remove_order_profile_order_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderproduct",
            name="count_product",
            field=models.PositiveIntegerField(
                default=1, verbose_name="Количество в заказе"
            ),
            preserve_default=False,
        ),
    ]