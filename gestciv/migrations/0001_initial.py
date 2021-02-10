# Generated by Django 2.2.7 on 2019-11-26 17:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppliNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateField(verbose_name='Date de publication')),
                ('news', models.TextField(verbose_name='Info')),
            ],
            options={
                'verbose_name': 'Software news (item)',
                'verbose_name_plural': 'Software news',
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Arrondissement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_arr', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code arrondissement')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom aronndissement')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Téléphone')),
                ('ca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nom_ca', to=settings.AUTH_USER_MODEL, verbose_name='Nom & Prénom du CA')),
            ],
            options={
                'verbose_name': 'Arrondissement',
                'verbose_name_plural': 'Arrondissements',
                'ordering': ['c_arr'],
            },
        ),
        migrations.CreateModel(
            name='BirthBrotherOrigin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Birth brother origin',
                'verbose_name_plural': 'Birth borther origins',
            },
        ),
        migrations.CreateModel(
            name='BirthCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Birth category',
                'verbose_name_plural': 'Birth categories',
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='BirthCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Birth condition',
                'verbose_name_plural': 'Birth conditions',
            },
        ),
        migrations.CreateModel(
            name='BirthTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Birth tag',
                'verbose_name_plural': 'Birth tags',
            },
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_dep', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code département')),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Département')),
            ],
            options={
                'verbose_name': 'Département',
                'verbose_name_plural': 'Départements',
                'ordering': ['c_dep'],
            },
        ),
        migrations.CreateModel(
            name='GeneralConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appli_name', models.TextField(default='Eregister', verbose_name='Software name')),
                ('default_country', django_countries.fields.CountryField(default='BJ', max_length=2, verbose_name='Default country')),
                ('nav_history', models.PositiveSmallIntegerField(default=10, verbose_name='Navigation history')),
            ],
            options={
                'verbose_name': 'Global settings of the software',
                'verbose_name_plural': 'Global settings of the software',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30, verbose_name='Description')),
                ('is_default', models.BooleanField(default=False, verbose_name='Default language')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Mairie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code commune')),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Nom commune')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Téléphone')),
                ('is_default', models.BooleanField(default=False, verbose_name='Default mairie')),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Département', to='gestciv.Departement', verbose_name='Département')),
                ('nom_maire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nom_maire', to=settings.AUTH_USER_MODEL, verbose_name='Nom & Prénom du maire')),
            ],
            options={
                'verbose_name': 'Commune',
                'verbose_name_plural': 'Communes',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(blank=True, max_length=255, null=True, upload_to='static/', verbose_name='Photo de profile')),
                ('profession', models.CharField(blank=True, default='', max_length=50)),
                ('phone', models.CharField(blank=True, default='', max_length=10)),
                ('organization', models.CharField(blank=True, default='', max_length=10, verbose_name='Lieu de travail')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profil_ville', to='gestciv.Arrondissement', verbose_name='Ville')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNavigationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessed_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=80)),
                ('url', models.CharField(max_length=255)),
                ('accessed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accede_par', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('nip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro identifiant privé')),
                ('title', models.CharField(choices=[('M.', 'M.'), ('MME', 'Mme')], default='M.', max_length=3, verbose_name='Civilité')),
                ('lastname', models.CharField(max_length=255, verbose_name='Nom')),
                ('young_girl_lastname', models.CharField(blank=True, max_length=30, verbose_name='Nom de jeune fille')),
                ('firstname', models.CharField(max_length=255, verbose_name='Prénom')),
                ('marital_status', models.CharField(choices=[('C', 'Célibataire'), ('M', 'Marié'), ('V', 'Veuf')], max_length=15, verbose_name='Stuation matrimoniale')),
                ('sex', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=8, verbose_name='Sexe')),
                ('birthday', models.DateField(verbose_name='Date de naissance')),
                ('birthcity', models.CharField(max_length=255, verbose_name='Ville de naissance')),
                ('nationality', django_countries.fields.CountryField(max_length=2, verbose_name='Pays de naissance')),
                ('job', models.CharField(max_length=30, verbose_name='Profession')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='rue et numéro, quartier, hameau, village')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Téléphone')),
                ('mail', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Mail')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_reside', to='gestciv.Mairie', verbose_name='Commune')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chef_quartier', to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arron_reside', to='gestciv.Arrondissement', verbose_name='Arrondissement')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_registration_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Personne',
                'unique_together': {('lastname', 'firstname', 'birthday')},
                'verbose_name_plural': 'Personnes',
                'ordering': ['lastname', 'firstname'],
            },
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_qua', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code arrondissement')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom quartier')),
                ('adresse', models.CharField(max_length=60, null=True, verbose_name='Adresse postale')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Téléphone')),
                ('arrondissement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quartier_arrondissement', to='gestciv.Arrondissement', verbose_name='arrondissement')),
                ('cq', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nom_cq', to=settings.AUTH_USER_MODEL, verbose_name='Nom & Prénom du CQ')),
            ],
            options={
                'verbose_name': 'Quartier',
                'verbose_name_plural': 'Quartier',
                'ordering': ['c_qua'],
            },
        ),
        migrations.CreateModel(
            name='Maternite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_mat', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Code arrondissement')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom maternité')),
                ('arrondissement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement', to='gestciv.Arrondissement', verbose_name='Arrondissement')),
            ],
            options={
                'verbose_name': 'Maternité',
                'verbose_name_plural': 'Maternités',
                'ordering': ['c_mat'],
            },
        ),
        migrations.CreateModel(
            name='BirthDeclaration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('nip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro identifiant privé')),
                ('sex', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=8, verbose_name='Sexe')),
                ('birthweight', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Poids à la naissance')),
                ('birthday', models.DateField(verbose_name='Date de naissance')),
                ('birthhour', models.TimeField(null=True, verbose_name='Heure de naissance')),
                ('birthcity', models.CharField(max_length=30, verbose_name='Ville de naissance')),
                ('birthcountry', django_countries.fields.CountryField(default='BJ', max_length=2, verbose_name='Pays de naissance')),
                ('bcduedate', models.DateField(blank=True, default=datetime.date(2019, 12, 17), null=True, verbose_name="Date d'échéance")),
                ('can_be_issued', models.BooleanField(default=False, verbose_name='can be issued')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birthdeclaration_add', to=settings.AUTH_USER_MODEL)),
                ('mairie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='new_birth_mairie', to='gestciv.Mairie', verbose_name='Mairie')),
                ('midwife', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sage_femme', to=settings.AUTH_USER_MODEL, verbose_name='Le médécin')),
                ('midwifegroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groupe_de_la_sage_femme', to='auth.Group', verbose_name='Groupe de travail')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birthdeclaration_update', to=settings.AUTH_USER_MODEL)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_birth_mother', to='gestciv.Registration', verbose_name='Mère')),
            ],
            options={
                'verbose_name': 'Déclaration',
                'verbose_name_plural': 'Déclarations',
            },
        ),
        migrations.CreateModel(
            name='BirthCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('nip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro identifiant privé')),
                ('firstname', models.CharField(max_length=30, verbose_name='Prénom(s)')),
                ('sex', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=8, verbose_name='Sexe')),
                ('birthweight', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Poids à la naissance')),
                ('birthday', models.DateField(verbose_name='Date de naissance')),
                ('birthhour', models.TimeField(null=True, verbose_name='Heure de naissance')),
                ('birthcountry', django_countries.fields.CountryField(default='BJ', max_length=2, verbose_name='Pays de naissance')),
                ('bcduedate', models.DateField(blank=True, default=datetime.date(2019, 12, 17), null=True, verbose_name="Date d'échéance")),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_birthcertif', to='gestciv.Mairie', verbose_name='Mairie')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birthcertificate_add', to=settings.AUTH_USER_MODEL)),
                ('declarant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declarantcertif', to='gestciv.Registration', verbose_name='Déclarant')),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fathercertif', to='gestciv.Registration', verbose_name='Father')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birthcertificate_update', to=settings.AUTH_USER_MODEL)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mothercertif', to='gestciv.Registration', verbose_name='Mère')),
            ],
            options={
                'verbose_name': 'Certificat de naissance',
                'verbose_name_plural': 'Certificats de naissances',
                'ordering': ['-bcduedate'],
            },
        ),
        migrations.CreateModel(
            name='Birth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('nip', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro identifiant privé')),
                ('firstname', models.CharField(max_length=30, verbose_name='Prénom(s)')),
                ('sex', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=8, verbose_name='Sexe')),
                ('birthweight', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Poids à la naissance')),
                ('birthday', models.DateField(verbose_name='Date de naissance')),
                ('birthhour', models.TimeField(null=True, verbose_name='Heure de naissance')),
                ('birthcountry', django_countries.fields.CountryField(default='BJ', max_length=2, verbose_name='Pays de naissance')),
                ('social_number', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='numero social')),
                ('bcduedate', models.DateField(blank=True, default=datetime.date(2019, 12, 17), null=True, verbose_name="Date d'échéance")),
                ('created', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_birth', to='gestciv.Mairie', verbose_name='Mairie')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birth_add', to=settings.AUTH_USER_MODEL)),
                ('declarant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declarant', to='gestciv.Registration', verbose_name='Déclarant')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement_birth', to='gestciv.Arrondissement', verbose_name='Arrondissement de naissance')),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='father', to='gestciv.Registration', verbose_name='Father')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gestciv_birth_update', to=settings.AUTH_USER_MODEL)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='gestciv.Registration', verbose_name='Mère')),
            ],
            options={
                'verbose_name': 'Naissance',
                'verbose_name_plural': 'Naissances',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='arrondissement',
            name='mairie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mairie', to='gestciv.Mairie', verbose_name='Commune'),
        ),
    ]
