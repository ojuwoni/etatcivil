# Generated by Django 2.2.8 on 2020-01-09 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestciv', '0045_auto_20200109_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mairie',
            name='departement',
        ),
        migrations.RemoveField(
            model_name='mairie',
            name='nom_maire',
        ),
        migrations.RemoveField(
            model_name='quartier',
            name='arrondissement',
        ),
        migrations.RemoveField(
            model_name='quartier',
            name='cq',
        ),
        migrations.AlterField(
            model_name='adoption',
            name='adoptioncountry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_adoption', to='geodivision.Mairie', verbose_name="Mairie d'adoption"),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='adoptiondistrict',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement_adoption', to='geodivision.Arrondissement', verbose_name="Arrondissement d'adoption"),
        ),
        migrations.AlterField(
            model_name='birth',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_birth', to='geodivision.Mairie', verbose_name='Mairie'),
        ),
        migrations.AlterField(
            model_name='birth',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement_birth', to='geodivision.Arrondissement', verbose_name='Arrondissement de naissance'),
        ),
        migrations.AlterField(
            model_name='birth',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='neighbor_birth', to='geodivision.Quartier', verbose_name='Lieu de naissance'),
        ),
        migrations.AlterField(
            model_name='birthcertificate',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_birthcertif', to='geodivision.Mairie', verbose_name='Mairie'),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groupe_de_la_sage_femme', to='geodivision.Arrondissement', verbose_name='Arrondissement de déclaration'),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='mairie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='new_birth_mairie', to='geodivision.Mairie', verbose_name='Mairie'),
        ),
        migrations.AlterField(
            model_name='birthdeclaration',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='neighbor_birth_dec', to='geodivision.Quartier', verbose_name='Lieu de naissance'),
        ),
        migrations.AlterField(
            model_name='maternite',
            name='arrondissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement', to='geodivision.Arrondissement', verbose_name='Arrondissement'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mairie_reside', to='geodivision.Mairie', verbose_name='Commune'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arron_reside', to='geodivision.Arrondissement', verbose_name='Arrondissement'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='neighbor_reside', to='geodivision.Quartier', verbose_name='Quartier'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profil_ville', to='geodivision.Arrondissement', verbose_name='Ville'),
        ),
        migrations.DeleteModel(
            name='Arrondissement',
        ),
        migrations.DeleteModel(
            name='Departement',
        ),
        migrations.DeleteModel(
            name='Mairie',
        ),
        migrations.DeleteModel(
            name='Quartier',
        ),
    ]
