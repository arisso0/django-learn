# Generated by Django 4.2.3 on 2023-07-31 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0005_alter_profile_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="avatars/", verbose_name="Аватар"
            ),
        ),
    ]