# Generated by Django 2.2.8 on 2019-12-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0018_auto_20191209_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='nom',
            field=models.CharField(max_length=100, unique=True, verbose_name='Profession'),
        ),
    ]
