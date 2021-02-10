# Generated by Django 2.2.7 on 2019-12-02 10:54

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0002_auto_20191130_0814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quartier',
            options={'ordering': ['nom'], 'verbose_name': 'Quartier/village', 'verbose_name_plural': 'Quartiers'},
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 23), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 23), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2019, 12, 23), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='quartier',
            name='c_qua',
            field=models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code village'),
        ),
        migrations.AlterField(
            model_name='quartier',
            name='cq',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nom_cq', to=settings.AUTH_USER_MODEL, verbose_name='Nom & Prénom du CQ/CV'),
        ),
    ]