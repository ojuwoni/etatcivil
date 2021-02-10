# Generated by Django 3.0.4 on 2021-02-08 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arrondissement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_arr', models.CharField(max_length=6, unique=True)),
                ('nom', models.CharField(max_length=30, verbose_name='Nom aronndissement')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
            ],
            options={
                'verbose_name': 'Arrondissement',
                'verbose_name_plural': 'Arrondissements',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_dep', models.CharField(max_length=2, unique=True)),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Département')),
            ],
            options={
                'verbose_name': 'Département',
                'verbose_name_plural': 'Départements',
                'ordering': ['nom'],
                'unique_together': {('c_dep', 'nom')},
            },
        ),
        migrations.CreateModel(
            name='GroupeEthnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.DecimalField(decimal_places=0, max_digits=4)),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Groupe ethnique')),
            ],
            options={
                'verbose_name': 'Groupe ethnique',
                'verbose_name_plural': 'Groupe ethnique',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code')),
                ('nom', models.CharField(max_length=50, unique=True, verbose_name='Profession')),
            ],
            options={
                'verbose_name': 'Profession',
                'verbose_name_plural': 'Professions',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_qua', models.CharField(max_length=8, unique=True)),
                ('nom', models.CharField(max_length=30, verbose_name='Nom quartier')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
                ('arrondissement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quartier_arrondissement', to='geodivision.Arrondissement', verbose_name='arrondissement')),
            ],
            options={
                'verbose_name': 'Quartier/village',
                'verbose_name_plural': 'Quartiers',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Mairie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_com', models.CharField(max_length=4, unique=True)),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Nom commune')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
                ('is_default', models.BooleanField(default=False, verbose_name='Default mairie')),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Département', to='geodivision.Departement', verbose_name='Département')),
            ],
            options={
                'verbose_name': 'Commune',
                'verbose_name_plural': 'Communes',
                'ordering': ['nom'],
            },
        ),
        migrations.AddField(
            model_name='arrondissement',
            name='mairie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mairie', to='geodivision.Mairie', verbose_name='Commune'),
        ),
    ]
