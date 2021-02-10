# Generated by Django 2.2.8 on 2019-12-10 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0019_auto_20191209_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='address',
        ),
        migrations.AddField(
            model_name='registration',
            name='comp_1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Complément 1'),
        ),
        migrations.AddField(
            model_name='registration',
            name='comp_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Complément 2'),
        ),
        migrations.AddField(
            model_name='registration',
            name='street_type',
            field=models.CharField(choices=[('Boulevard', 'Boulevard'), ('Avenue', 'Avenue'), ('Cours', 'Cours'), ('Place', 'Place'), ('Rue', 'Rue'), ('Route', 'Route'), ('Voie', 'Voie'), ('Chemin', 'Chemin'), ('Square', 'Square'), ('Impasse', 'Impasse'), ('Rond-point', 'Rond-point'), ('Quai', 'Quai')], default='Rue', max_length=30, verbose_name='Type de rue'),
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 31), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 31), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 31), null=True, verbose_name="Date d'échéance"),
        ),
    ]
