# Generated by Django 2.2.8 on 2019-12-03 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0008_auto_20191203_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='nom',
            field=models.CharField(max_length=50, unique=True, verbose_name='Profession'),
        ),
    ]
