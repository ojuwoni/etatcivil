# Generated by Django 2.2.8 on 2020-01-04 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0041_auto_20200104_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birth',
            name='birthcountry',
        ),
    ]
