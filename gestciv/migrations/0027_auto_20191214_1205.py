# Generated by Django 2.2.8 on 2019-12-14 12:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0026_auto_20191213_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupeEthnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.DecimalField(decimal_places=0, max_digits=4)),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Groupe ethnique')),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='father_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom/Prénom du père'),
        ),
        migrations.AddField(
            model_name='registration',
            name='mother_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom/Prénom de la mère'),
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 4), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 4), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 4), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AddField(
            model_name='registration',
            name='ethnie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ethnie_reside', to='gestciv.GroupeEthnique', verbose_name='Ethnie'),
        ),
    ]
