# Generated by Django 2.2.8 on 2019-12-03 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0013_auto_20191203_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='nom',
            field=models.CharField(max_length=200, unique=True, verbose_name='Profession'),
        ),
    ]
