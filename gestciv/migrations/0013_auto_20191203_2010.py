# Generated by Django 2.2.8 on 2019-12-03 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0012_auto_20191203_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='nom',
            field=models.CharField(max_length=150, unique=True, verbose_name='Profession'),
        ),
    ]
