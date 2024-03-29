# Generated by Django 3.0.3 on 2020-02-26 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0053_auto_20200220_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='marital_status',
        ),
        migrations.AddField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('C', 'Célibataire'), ('M', 'Marié'), ('V', 'Veuf'), ('I', 'Décédé'), ('D', 'Divorcé')], default='M', max_length=15, verbose_name='Stuation'),
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 18), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 18), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 18), null=True, verbose_name="Date d'échéance"),
        ),
    ]
