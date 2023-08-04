# Generated by Django 4.2.3 on 2023-07-26 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_remove_order_payment_remove_payment_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Платежная карта', 'verbose_name_plural': 'Платежные карты'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterField(
            model_name='basket',
            name='count',
            field=models.IntegerField(verbose_name='Количество товара'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='total_price',
            field=models.FloatField(verbose_name='Итоговая сумма'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='basketproduct',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='basketproduct',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=300, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('COURIER', 'Курьер'), ('PICKUP', 'Самовывоз')], default='PICKUP', max_length=8, verbose_name='Доставка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('CARD', 'Моя карта'), ('OTHER', 'Другое')], max_length=8, null=True, verbose_name='Тип оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый'), ('PAID', 'Оплачен'), ('WORK', 'В работе'), ('DONE', 'Доставлен')], default='NEW', max_length=8, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.FloatField(verbose_name='Итоговая сумма'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='code',
            field=models.CharField(max_length=4, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='month',
            field=models.CharField(max_length=2, verbose_name='Месяц'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=1000, verbose_name='Имя держателя'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='number',
            field=models.CharField(max_length=16, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='year',
            field=models.CharField(max_length=4, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='media/default_avatar.jpg', upload_to='avatars/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(max_length=1000, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
    ]
