# Generated by Django 3.0.3 on 2020-03-27 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Комментарий к заказу'),
        ),
    ]