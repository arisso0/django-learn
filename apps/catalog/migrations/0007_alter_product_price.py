# Generated by Django 4.2.3 on 2023-07-31 08:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_image_src"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Цена"
            ),
        ),
    ]
