# Generated by Django 3.0.3 on 2020-04-07 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200405_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='subtitle',
            new_name='short_text',
        ),
    ]
