# Generated by Django 3.0.3 on 2020-04-10 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auto_20200410_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='goods',
        ),
        migrations.AddField(
            model_name='cart',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Итоговая цена в корзине'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.CreateModel(
            name='GoodsInCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Общая сумма')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Общая сумма')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='app.Cart', verbose_name='Корзина')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goods', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]
