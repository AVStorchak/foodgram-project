# Generated by Django 3.0.8 on 2021-02-06 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210204_1605'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
