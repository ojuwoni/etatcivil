# Generated by Django 2.2.8 on 2019-12-15 10:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0031_registration_arrived_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='dead',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 5), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 5), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 5), null=True, verbose_name="Date d'échéance"),
        ),
    ]
