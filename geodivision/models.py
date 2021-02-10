from django.urls import reverse_lazy, reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup
from django.db.models.signals import post_save
from django.dispatch import receiver


class GroupeEthnique(models.Model):
	code		= models.DecimalField(max_digits=4,  decimal_places=0)
	nom		= models.CharField(max_length=30, null=False, unique=True, verbose_name='Groupe ethnique')

	def clean(self):
                super().clean()

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ['nom']
		verbose_name = _("Groupe ethnique")
		verbose_name_plural = _("Groupe ethnique")

class Departement(models.Model):

        c_dep           = models.CharField(max_length=2, null=False, unique=True)
        nom             = models.CharField(max_length=30, null=False, unique=True, verbose_name='Département')

        def clean(self):
                super().clean()

        def __str__(self):
                return self.nom

        class Meta:
                unique_together = ['c_dep', 'nom']
                ordering = ['nom']
                verbose_name = _("Département")
                verbose_name_plural = _("Départements")


class Profession(models.Model):
	code            = models.DecimalField(max_digits=4,  decimal_places=0, verbose_name="Code")
	nom             = models.CharField(max_length=50, null=False, unique=True, verbose_name='Profession')


	def __str__(self):
		return self.nom

	class Meta:
		ordering = ['nom']
		verbose_name = _("Profession")
		verbose_name_plural = _("Professions")



class Mairie(models.Model):

	c_com		= models.CharField(max_length=6, null=False, unique=True)
	departement     = models.ForeignKey(Departement, related_name='Département', verbose_name='Département',
	                               on_delete=models.CASCADE, null=False)
#	nom_maire	= models.ForeignKey(DjangoUser, related_name='nom_maire', verbose_name='Nom & Prénom du maire',
					#on_delete=models.CASCADE, null=False)
	nom		= models.CharField(max_length=30, null=False, unique=True, verbose_name='Nom commune')
	adresse		= models.CharField(max_length=60, null=True, unique=False, verbose_name='Adresse postale')
	is_default 	= models.BooleanField(_("Default mairie"), default=False)

	@staticmethod
	def get_default_mairie():
		if Mairie.objects.filter(is_default=True):
			return Mairie.objects.filter(is_default=True)[0]
		else:
		#	raise ValidationError({'mairie': ugettext("Mairie par défaut non définie.")})
			return None

	def __str__(self):
		return self.nom

	class Meta:
                ordering = ['nom']
                verbose_name = _("Commune")
                verbose_name_plural = _("Communes")


class Arrondissement(models.Model):

    c_arr	= models.CharField(max_length=10, null=False, unique=True)
    mairie	= models.ForeignKey(Mairie, related_name='mairie', verbose_name='Commune',
                           on_delete=models.CASCADE, null=False)
    nom		= models.CharField(max_length=30, null=False, verbose_name='Nom aronndissement')
    adresse	= models.CharField(max_length=60, null=True, unique=False, verbose_name='Adresse postale')


    def clean(self):
        super().clean()

    def __str__(self):
        return self.nom

    @staticmethod
    def get_arrondissement():
        if Mairie.get_default_mairie() is not None :
            return (Arrondissement.objects.filter(mairie_id= Mairie.get_default_mairie().id))

    class Meta:
        ordering = ['nom']
        verbose_name = _("Arrondissement")
        verbose_name_plural = _("Arrondissements")

class Quartier(models.Model):

	c_qua           = models.CharField(max_length=14, null=False, unique=True)
	arrondissement  = models.ForeignKey(Arrondissement, related_name='quartier_arrondissement', verbose_name='arrondissement',
                            on_delete=models.CASCADE, null=False)
	nom             = models.CharField(max_length=50, null=False, verbose_name='Nom quartier')
	adresse         = models.CharField(max_length=60, null=True, unique=False, verbose_name='Adresse postale')

	def clean(self):
		super().clean()

	def __str__(self):
		return self.nom

	class Meta:
            ordering = ['nom']
            verbose_name = _("Quartier/village")
            verbose_name_plural = _("Quartiers")


