# Generated by Django 3.0.3 on 2020-04-15 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20200414_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='goodsincart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Cart', verbose_name='Товар в корзине'),
        ),
    ]