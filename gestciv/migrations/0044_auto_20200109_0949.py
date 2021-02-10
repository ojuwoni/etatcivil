# Generated by Django 2.2.8 on 2020-01-09 09:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0043_auto_20200105_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 30), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 30), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 30), null=True, verbose_name="Date d'échéance"),
        ),
    ]
