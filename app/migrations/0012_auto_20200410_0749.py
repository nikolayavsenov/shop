# Generated by Django 3.0.3 on 2020-04-10 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_cart_total_price'),
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
    ]