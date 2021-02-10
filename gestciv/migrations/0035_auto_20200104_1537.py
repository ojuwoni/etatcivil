# Generated by Django 2.2.8 on 2020-01-04 15:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestciv', '0034_auto_20191226_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fetaldeath',
            old_name='nip',
            new_name='mother',
        ),
        migrations.AlterField(
            model_name='birth',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='bcduedate',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), null=True, verbose_name="Date d'échéance"),
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('weddingplace', models.DateField(verbose_name='Lieu de mariage')),
                ('weddingday', models.DateField(verbose_name='Date de mariage')),
                ('recordingday', models.DateField(verbose_name='Date d\\enregistrement ')),
                ('certificate_num', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Certificat de mariage')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_wedding_add', to=settings.AUTH_USER_MODEL)),
                ('husband', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='husband_wedding', to='gestciv.Registration', verbose_name='Husband')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_wedding_update', to=settings.AUTH_USER_MODEL)),
                ('wife', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wife_wedding', to='gestciv.Registration', verbose_name='Wife')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Separation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('separationplace', models.DateField(verbose_name='Lieu de séparation')),
                ('separationday', models.DateField(verbose_name='Date de séparation')),
                ('recordingday', models.DateField(verbose_name='Date d\\enregistrement ')),
                ('certifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certifier_separation', to=settings.AUTH_USER_MODEL, verbose_name='Autorité agissante')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_separation_add', to=settings.AUTH_USER_MODEL)),
                ('husband', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='husband_separation', to='gestciv.Registration', verbose_name='Husband')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_separation_update', to=settings.AUTH_USER_MODEL)),
                ('wife', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wife_separation', to='gestciv.Registration', verbose_name='Wife')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Divorced',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('weddingplace', models.DateField(verbose_name='Lieu de mariage')),
                ('weddingday', models.DateField(verbose_name='Date de mariage')),
                ('recordingday', models.DateField(verbose_name="Date d'enregistrement ")),
                ('certificate_num', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Certificat de mariage')),
                ('num_depend_child', models.DecimalField(decimal_places=0, max_digits=2, verbose_name="Nombre d'enfants à charge")),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_divorced_add', to=settings.AUTH_USER_MODEL)),
                ('husband', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='husband_divorced', to='gestciv.Registration', verbose_name='Husband')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_divorced_update', to=settings.AUTH_USER_MODEL)),
                ('wife', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wife_divorced', to='gestciv.Registration', verbose_name='Wife')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adoption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('nip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro identifiant privé')),
                ('adoptioncountry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_adoption', to='gestciv.Mairie', verbose_name="Mairie d'adoption")),
                ('adoptiondistrict', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement_adoption', to='gestciv.Arrondissement', verbose_name="Arrondissement d'adoption")),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_adoption_add', to=settings.AUTH_USER_MODEL)),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='father_adoption', to='gestciv.Registration', verbose_name='Père adoptif')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_adoption_update', to=settings.AUTH_USER_MODEL)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother_adoption', to='gestciv.Registration', verbose_name='Mère adoptive')),
            ],
            options={
                'verbose_name': 'Adoption',
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Adoptions',
            },
        ),
    ]