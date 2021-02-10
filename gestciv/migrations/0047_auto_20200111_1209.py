# Generated by Django 2.2.8 on 2020-01-11 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0046_auto_20200109_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 1), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 1), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 1), null=True, verbose_name="Date d'échéance"),
        ),
    ]
