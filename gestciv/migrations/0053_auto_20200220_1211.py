# Generated by Django 3.0.3 on 2020-02-20 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0052_auto_20200206_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 12), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birth',
            name='birthtype',
            field=models.CharField(blank=True, choices=[('Simple', 'Simple'), ('Jumeau', 'Jumeau'), ('Triplé', 'Triplé'), ('Quadruplé', 'Quadruplé'), ('Autre', 'Autre')], default='Simple', max_length=20, null=True, verbose_name='Type de naissance'),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 12), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 12), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='birthtype',
            field=models.CharField(blank=True, choices=[('Simple', 'Simple'), ('Jumeau', 'Jumeau'), ('Triplé', 'Triplé'), ('Quadruplé', 'Quadruplé'), ('Autre', 'Autre')], default='Simple', max_length=20, null=True, verbose_name='Type de naissance'),
        ),
    ]
