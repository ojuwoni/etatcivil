from django.urls import reverse_lazy, reverse
from django.db import models
from datetime import datetime, timedelta, date
from django_countries.fields import CountryField
from django.forms import ModelChoiceField, ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from random import randint
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as DjangoGroup
from django.db.models import Q
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from geodivision.models import GroupeEthnique,Arrondissement,Mairie,Quartier
from django.conf import settings
import string
import uuid

STATUS_CHOICES=(
	('C','Célibataire'),
	('M','Marié'),
	('V','Veuf'),
        ('I','Décédé'),
        ('D','Divorcé'))

CIVILITY_CHOICES=(
	('M.', 'M.'),
	('MME', 'Mme')
	)

SEX_CHOICES=(
	('M','Masculin'),
	('F', 'Féminin')
	)

BIRTH_TYPE=(
	('Simple','Simple'),
	('Jumeau','Jumeau'),
	('Triplé','Triplé'),
	('Quadruplé','Quadruplé'),
	('Autre','Autre'))


class GeneralConfiguration(models.Model):
    appli_name = models.TextField(verbose_name=_("Software name"), default=u"Eregister")
    default_country = CountryField(verbose_name=_("Default country"), default="BJ")
    nav_history = models.PositiveSmallIntegerField(_("Navigation history"), default=10)

    def __str__(self):
        return ugettext("Configuration")  # TODO: check if it could be lazy

    class Meta:
        verbose_name = _("Global settings of the software")
        verbose_name_plural = verbose_name



class UserNavigationHistoryManager(models.Manager):
    def get_list(self, user):
        return self.filter(accessed_by=user).order_by('accessed_by')


class UserNavigationHistory(models.Model):
    NAV_HISTORY = 10

    accessed_by = models.ForeignKey(DjangoUser, related_name='accede_par', on_delete=models.CASCADE)
    accessed_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    url = models.CharField(max_length=255)

    objects = UserNavigationHistoryManager()

    @staticmethod
    def add(url, title, user):
        lst = UserNavigationHistory.objects.get_list(user)
        h = UserNavigationHistory(url=url, title=title, accessed_by=user)
        h.save()

    @staticmethod
    def exist_url(url):
        return UserNavigationHistory.objects.filter(url=url).count() > 0

#############


class ReferenceEntity(models.Model):
    label = models.CharField(u"Description", max_length=30)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


#########
# Model #
#########

class ModelEntity(models.Model):
    created_by = models.ForeignKey(DjangoUser, related_name="%(app_label)s_%(class)s_add", on_delete=models.PROTECT, null=True, blank=True)
    created_on = models.DateTimeField(verbose_name=u"Créé le", auto_now_add=True)
    modified_by = models.ForeignKey(DjangoUser, related_name="%(app_label)s_%(class)s_update", null=True, blank=True, on_delete=models.PROTECT)
    modified_on = models.DateTimeField(verbose_name=u"Modifié le", auto_now=True, null=True, blank=True)

    def clean(self):
        super(ModelEntity, self).clean()

    def save(self, *args, **kwargs):
        super(ModelEntity, self).save(*args, **kwargs)

    class Meta:
       abstract = True


class Language(ReferenceEntity):
    is_default = models.BooleanField(_("Default language"), default=False)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    @staticmethod
    def get_default_language():
        if Language.objects.count() > 0:
            return Language.objects.filter(is_default=True)[0]
        else:
            return None




################################################
#
# Fonction de création d'un groupe à partir 
# d'un signal reçu lors de la  création d'une commune 
# ou d'un arrondissement
#######################################################
def CreateGroup(sender, instance, **kwargs):
	new_group = instance
	if kwargs["created"]:
		new_group, created = Group.objects.get_or_create(name=new_group)


class Profession(models.Model):
	code            = models.DecimalField(max_digits=4,  decimal_places=0, verbose_name="Code")
	nom             = models.CharField(max_length=50, null=False, unique=True, verbose_name='Profession')


	def __str__(self):
		return self.nom

	class Meta:
		ordering = ['nom']
		verbose_name = _("Profession")
		verbose_name_plural = _("Professions")



#######################################################################
#
# Définition d'un profil utilisateur spécifique à ce projet
#
########################################################################
class UserProfile(models.Model):
	user		=	models.OneToOneField(User, related_name='User', on_delete=models.CASCADE)
	photo		=	models.FileField(verbose_name=("Photo de profile"),upload_to='static/', 
						max_length=255, null=True, blank=True)
	profession	=	models.CharField(default='', max_length=50, blank=True)
	phone		=	models.CharField(default='', max_length=10, blank=True)
	organization	=	models.CharField(default='', max_length=10, verbose_name='Lieu de travail', blank=True)
	city		= 	models.ForeignKey(Arrondissement, related_name='profil_ville', verbose_name='Ville',
					on_delete=models.CASCADE, null=True, blank=True)


def  CreateProfile(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = UserProfile(user=user)
		user_profile.save()

post_save.connect(CreateProfile, sender=User)

######################################################################

class PublishedManager(models.Manager):

        def get_queryset(self):
                return super(PublishedManager, self).get_queryset().filter(status='published')


class RegistrationManager(models.Manager):
    def get_by_first_and_last_name(self, firstname, lastname, birthday):
        return self.filter(firstname__iexact=firstname, lastname__iexact=lastname).first()


    def search(self, nip='', name=''):
        r_list = self.all()
        if nip != '':
            r_list  = r_list.filter(nip__istartswith = nip)
        if name != '':
            r_list = r_list.filter(Q(lastname__istartswith=name) | Q(firstname__istartswith=name) )
        return r_list

    def is_single(self):
       if self.objects.search(self.nip).filter(status = 'C') is not None:
          return "Célibataire"
       return "Marié"


class Registration(ModelEntity):


	STREET_TYPE_CHOICES = (
		('Boulevard', 'Boulevard'),
		('Avenue', 'Avenue'),
		('Cours', 'Cours'),
		('Place', 'Place'),
		('Rue', 'Rue'),
		('Route', 'Route'),
		('Voie', 'Voie'),
		('Chemin', 'Chemin'),
		('Square', 'Square'),
		('Impasse', 'Impasse'),
		('Rond-point', 'Rond-point'),
		('Quai', 'Quai')
	)



	nip 		            = models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	title                       = models.CharField(max_length=3, choices=CIVILITY_CHOICES, default='M.', verbose_name="Civilité")
	lastname                    = models.CharField(max_length=255, verbose_name='Nom')
	young_girl_lastname         = models.CharField(max_length=30, verbose_name='Nom de jeune fille', blank=True)
	firstname                   = models.CharField(max_length=255, verbose_name='Prénom')
	ice	                    = models.ForeignKey("self", related_name='ice_registration', verbose_name='Personne à joindre', 
					on_delete=models.CASCADE, null=True, blank=True)
	status                      = models.CharField(max_length=15, choices=STATUS_CHOICES, default='M',verbose_name='Stuation')
	sex                         = models.CharField(max_length=8, choices=SEX_CHOICES, 
                                            default='F', null=True, blank=True, verbose_name='Sexe')
	birthday                    = models.DateField(verbose_name='Date de naissance')
	nationality                 = CountryField(max_length=255, verbose_name='Pays de naissance', default="BJ")
	job                         = models.ForeignKey(Profession, related_name='profession_reg', 
						on_delete=models.CASCADE, verbose_name='Profession')
	father_name		    = models.CharField(max_length=255, verbose_name='Nom/Prénom du père', null=True, blank=True)
	mother_name		    = models.CharField(max_length=255, verbose_name='Nom/Prénom de la mère', null=True, blank=True)
	ethnie 			    =  models.ForeignKey(GroupeEthnique, related_name='ethnie_reside', 
                                        null=True, blank=True, verbose_name='Ethnie', on_delete=models.CASCADE)
	arrived_date                = models.DateField(verbose_name='Date d\'arrivée', null=True, blank=True)
	city	       		    =  models.ForeignKey(Mairie, related_name='mairie_reside', null=True, blank=True, verbose_name='Commune', 
						on_delete=models.CASCADE)
	district                    = models.ForeignKey(Arrondissement, related_name='arron_reside', null=True, blank=True, 
						verbose_name='Arrondissement', on_delete=models.CASCADE)
	neighborhood                    = models.ForeignKey(Quartier, related_name='neighbor_reside', null=True, blank=True,
						 verbose_name='Quartier', on_delete=models.CASCADE)
	street_type 		    = models.CharField(max_length=30, verbose_name="Type de rue", null=True, blank=True,
					   choices=STREET_TYPE_CHOICES, default='Rue')
	comp_1 			    = models.CharField(max_length=255, verbose_name="Complément 1", blank=True, null=True)
	comp_2 			    = models.CharField(max_length=255, verbose_name="Complément 2", blank=True, null=True)
	dead			    = models.BooleanField(default=False, null=True, blank=True)
	phone                       = models.CharField(max_length=255, blank=True, null=True, verbose_name='Téléphone')
	mail                        = models.EmailField(max_length=255, verbose_name='Mail', blank=True, null=True)
	is_dead                     = models.BooleanField(default=False, null=True, blank=True)
	created_by      	    = models.ForeignKey(DjangoUser, related_name='chef_quartier', 
                                        on_delete=models.CASCADE, null=True, blank=True)
	created                     = models.DateTimeField(auto_now_add=True)
	updated                     = models.DateTimeField(auto_now_add=True)


	objects = RegistrationManager()

	def save(self, *args, **kwargs):
		
		self.lastname = self.lastname.strip().title()
		self.firstname = self.firstname.strip().title()
		if self.status == 'I':
			self.id_dead = True
		if self.young_girl_lastname:
			self.young_girl_lastname = self.young_girl_lastname.strip().title()
		self.full_clean()

		#################################################################
		# MAJ du nip/birthnum						#
		################################################################
		#Homme = 1 / Femme = 2
		sex_number = []
		if self.sex == 'M' :
			sex_number = 1
		elif self.sex == 'F' :
			sex_number = 2

		#Récupère année de naissance
		birthyear_temp = str(self.birthday.year)
		birthyear_temp2 = str(birthyear_temp.split(" "))
		birthyear = birthyear_temp2[4] + birthyear_temp2[5]

		#Récupère mois de naissance
		birthmonth_temp = self.birthday.month
		if len(str(birthmonth_temp)) == 1 :
			birthmonth = '0' + str(birthmonth_temp)
		else :
			birthmonth = birthmonth_temp

		# #Récupère première lettre prénom 
		firstname = self.firstname[0]

		#Récupère N° Mairie (ici récupère nom mais sera changé en n°)
		birth_mairie = self.city.code

		#Génère un nombre aléaloire :
		key_temp = randint(0,999999)
		if len(str(key_temp)) == 1 :
			key = '00000' + str(key_temp)
		elif len(str(key_temp)) == 2 :
			key = '0000' + str(key_temp)
		elif len(str(key_temp)) == 3 :
			key = '000' + str(key_temp)
		elif len(str(key_temp)) == 4 :
			key = '00' + str(key_temp)
		elif len(str(key_temp)) == 5 :
			key = '0' + str(key_temp)
		else :
			key = key_temp

		birth_nip = str(birthyear) + \
					str(birthmonth) + \
						str(birth_mairie) + \
								str(firstname) + \
									str(sex_number)+\
										str(key)

		self.nip = birth_nip
		super(Registration, self).save(*args, **kwargs)


	def get_full_name(self):
		if not self.firstname:
			return ""
		full_name = ' '.join([self.firstname, self.lastname, str(self.birthday)])
		if self.young_girl_lastname:
			full_name += '(' + self.young_girl_lastname + ')'
		return full_name


	def get_absolute_url(self):
		return reverse('gestciv:registration_update', kwargs={'pk':self.pk})

	def get_article_type(self):
		article = ''
		terminaison = ''
		pronom = ''
		if self.title == 'M.':
			article = 'le'
			terminaison = ''
			pronom = 'il'
		elif self.title == 'MME':
			article = 'la'
			terminaison = 'e'
			pronom = 'elle'
		context= {'article':article, 'terminaison':terminaison, 'pronom':pronom}
		return context 

	def is_minor(self):
		today = date.today()
		birthday = self.birthday
		return (today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))) < settings.ADULTE

	def is_single(self):
		if self.status == 'C':
			return "Célibataire"
		return "Marié"

	def age(self):
		today = date.today()
		birthday = self.birthday
		return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

	def get_children(self):
		return self.birth_set.firstname

	def __str__(self):
		return self.get_full_name()

	class Meta:
		unique_together = [[ 'lastname','firstname','birthday' ]]
		ordering = ['lastname', 'firstname']
		verbose_name = _("Personne")
		verbose_name_plural = _("Personnes")


class Maternite(models.Model):

	c_mat           = models.DecimalField(max_digits=4,  decimal_places=0, verbose_name="Code arrondissement")
	arrondissement  = models.ForeignKey(Arrondissement, related_name='arrondissement', verbose_name='Arrondissement',
				on_delete=models.CASCADE, null=False)
	nom             = models.CharField(max_length=30, null=False, verbose_name='Nom maternité')

	def clean(self):
		super().clean()

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ['c_mat']
		verbose_name = _("Maternité")
		verbose_name_plural = _("Maternités")



class BirthDeclarationManager(models.Manager):

	def list_brothers_by_mother(self, pk):
	#Todo: Si le parent etait la mère
		return BirthDeclaration.objects.filter(mother__id=pk)

	def search(self, nip, birthcity='', birthcountry='', sex='', birthday='', mother=''):
		r_list = self.all()

		if nip != '':
			r_list = r_list.filter(nip__icontains=nip)
		if birthcity != '':
			r_list = r_list.filter(birthcity=birthcity)
		if sex != '':
			r_list = r_list.filter(sex__icontains=sex)
		if birthday != '':
			r_list = r_list.filter(birthday__icontains=birthday)
		if mother != '':
			r_list = (
				r_list.filter(registration__lastname__icontains=mother__lastname, 
					registration__sex__icontains='F')
				)

		return r_list

###############################################################################
#
# BirthDeclaration: Cette table est utilisée par la maternité (le médécin)
#			responsable de l'accouchement, il a pour obligation  
#			de déclarer la nouvelle naissance et expédie 
#			le formulaire à l'arrondissement dont dépent 
#			établissement.
###############################################################################
class BirthDeclaration(ModelEntity):


	nip		= models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	sex             = models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe')
	birthweight     = models.DecimalField(max_digits=4,  decimal_places=2, verbose_name="Poids à la naissance")
	birthday        = models.DateField(null=False, verbose_name='Date de naissance')
	birthhour       = models.TimeField(null=True, verbose_name='Heure de naissance')
	mother          = models.ForeignKey(Registration, related_name='new_birth_mother', verbose_name='Mère',
				on_delete=models.CASCADE, null=False)
	mairie 		=  models.ForeignKey(Mairie, related_name='new_birth_mairie', verbose_name='Mairie',
				on_delete=models.PROTECT, null=True, blank=True)
	midwife	        = models.ForeignKey(DjangoUser, related_name='sage_femme', 
				verbose_name="Le médécin", on_delete=models.CASCADE, null=True)
	district	= models.ForeignKey(Arrondissement, verbose_name="Arrondissement de déclaration", related_name='groupe_de_la_sage_femme', 
				on_delete=models.CASCADE, null=True)
	neighborhood    = models.ForeignKey(Quartier, related_name='neighbor_birth_dec', null=True, blank=True,
				verbose_name='Lieu de naissance', on_delete=models.CASCADE)
	birthtype	= models.CharField(max_length=20, choices=BIRTH_TYPE, verbose_name="Type de naissance", 
				default='Simple', null=True, blank=True)
	bcduedate	= models.DateField(default=(date.today() + timedelta(days=21)), verbose_name="Date d\'échéance", null=True, blank=True)
	can_be_issued	= models.BooleanField(_("can be issued"), default=False)

	objects = BirthDeclarationManager()


	def save(self, *args, **kwargs):
		
		self.full_clean()

		#################################################################
		# MAJ du nip/birthnum						#
		################################################################
		#Homme = 1 / Femme = 2
		sex_number = []
		if self.sex == 'M' :
			sex_number = 1
		elif self.sex == 'F' :
			sex_number = 2

		#Récupère année de naissance
		birthyear_temp = str(self.birthday.year)
		birthyear_temp2 = str(birthyear_temp.split(" "))
		birthyear = birthyear_temp2[4] + birthyear_temp2[5]

		#Récupère mois de naissance
		birthmonth_temp = self.birthday.month
		if len(str(birthmonth_temp)) == 1 :
			birthmonth = '0' + str(birthmonth_temp)
		else :
			birthmonth = birthmonth_temp

		# #Récupère première lettre prénom 
		firstname = self.alphabet_position(self.mother.firstname[0])

		#Récupère N° Mairie (ici récupère nom mais sera changé en n°)
		birth_mairie = self.mairie.code

		#Génère un nombre aléaloire :
		key_temp = randint(0,999999)
		if len(str(key_temp)) == 1 :
			key = '00000' + str(key_temp)
		elif len(str(key_temp)) == 2 :
			key = '0000' + str(key_temp)
		elif len(str(key_temp)) == 3 :
			key = '000' + str(key_temp)
		elif len(str(key_temp)) == 4 :
			key = '00' + str(key_temp)
		elif len(str(key_temp)) == 5 :
			key = '0' + str(key_temp)
		else :
			key = key_temp

		birth_nip = str(birthyear) + \
					str(birthmonth) + \
						str(birth_mairie) + \
								str(firstname) + \
									str(sex_number)+\
										str(key)

		self.nip = birth_nip
		super(BirthDeclaration, self).save(*args, **kwargs)
###################################################################################################

	def alphabet_position(self,text_string):
		dict1 = {value: (int(key) + 1) for key, value in enumerate(list(string.ascii_lowercase))}
		return " ".join([str(dict1[alp]) for alp in list(text_string.lower()) if alp.isalpha()])


	def is_late(self):
		if self.bcduedate >= date.today():
			self.can_be_issued=True
		return self.can_be_issued

	def clean(self):
		super(BirthDeclaration, self).clean()

	def get_absolute_url(self):
		return reverse('gestciv:birth_update', kwargs={'pk':self.pk})

	def __str__(self):
		return self.nip

	class Meta:
		verbose_name = _("Déclaration")
		verbose_name_plural = _("Déclarations")



class BirthCondition(ReferenceEntity):
    class Meta:
        verbose_name = _("Birth condition")
        verbose_name_plural = _("Birth conditions")


class DeathManager(models.Manager):

    def search(self, person='', eventlocation='', reglocation=''):
        r_list = self.all()
        if person != '':
            r_list = r_list.filter(person=person)
        if eventlocation != '':
            r_list = r_list.filter(eventlocation=eventlocation)
        if reglocation != '':
            r_list = r_list.filter(eventlocation=eventlocation)

        return r_list


###############################################################################
#
# Death : 
#	
#
#
#
###############################################################################
class Death(ModelEntity):

	nip             = models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	person          = models.ForeignKey(Registration, related_name='death_registration', verbose_name='Administré',
                                on_delete=models.CASCADE, null=False)
	eventlocation   = models.CharField(max_length=30, null=False, verbose_name='Lieu de décès')
	reglocation     = models.CharField(max_length=30, null=False, verbose_name='Lieu d\'enregistrement')
	cause	        = models.CharField(max_length=30, null=False, verbose_name='cause du décès')
	deathday        = models.DateField(null=False, verbose_name='Date de décès')
	certifier	= models.ForeignKey(DjangoUser, related_name='certifier_death' ,
				verbose_name="Le certificateur", on_delete=models.CASCADE, null=True)

	objects = DeathManager()


	def save(self, *args, **kwargs):
		
		self.full_clean()

		super(Death, self).save(*args, **kwargs)

	def clean(self):
		super(Death, self).clean()

	def get_absolute_url(self):
		return reverse('gestciv:death_update', kwargs={'pk':self.pk})

	def __str__(self):
		return self.nip

	class Meta:
		verbose_name = _("Décès")
		verbose_name_plural = _("Décès")


class FetalDeathManager(models.Manager):

    def search(self, nip='', eventlocation='', certifier=''):
        r_list = self.all()
        if nip != '':
            r_list = r_list.filter(nip=nip)
        if eventlocation != '':
            r_list = r_list.filter(eventlocation=eventlocation)
        if certifier != '':
            r_list = r_list.filter(certifier=certifier)

        return r_list


###############################################################################
#
# Fetal Death : 
#	
#
#
#
###############################################################################
class FetalDeath(ModelEntity):

	mother	          = models.ForeignKey(Registration, related_name='mother_death_registration', verbose_name='NIP de la mère',
                                on_delete=models.CASCADE, null=False)
	deathday        = models.DateField(null=False, verbose_name='Date de décès')
	eventlocation	= models.CharField(max_length=30, null=False, verbose_name='Lieu de décès')
	regday	     	= models.CharField(max_length=30, null=False, verbose_name='Lieu d\'enregistrement')
	cause	        = models.CharField(max_length=30, null=False, verbose_name='cause du décès')
	certifier	= models.ForeignKey(DjangoUser, related_name='certifier_fetaldeath' ,
				verbose_name="Le certificateur", on_delete=models.CASCADE, null=True)

	objects = DeathManager()


	def save(self, *args, **kwargs):
		
		self.full_clean()

		super(FetalDeath, self).save(*args, **kwargs)

	def clean(self):
		super(FetalDeath, self).clean()

	def get_absolute_url(self):
		return reverse('gestciv:fetaldeath_update', kwargs={'pk':self.pk})

	def __str__(self):
		return self.nip

	class Meta:
		verbose_name = _("Mort foetale")
		verbose_name_plural = _("Morts foetales")





class BirthCategory(ReferenceEntity):
    # For example : simple, jumeaux, triplés, quadruplés
    class Meta:
        verbose_name = _("Birth category")
        verbose_name_plural = _("Birth categories")
        ordering = ['label']

class BirthTag(ReferenceEntity):
    class Meta:
        verbose_name = _("Birth tag")
        verbose_name_plural = _("Birth tags")


class BirthBrotherOrigin(ReferenceEntity):
    class Meta:
        verbose_name = _("Birth brother origin")
        verbose_name_plural = _("Birth borther origins")



######################################################################
#
# Birth: Cette table permet de constituer par l'officier administratif
#	l'acte de naissance du nouveau né.
#	L'officier traitant reçoit les informations nécessaires de la 
#	table BirthDeclaration
#######################################################################
class BirthManager(models.Manager):

    def list_childs_by_father(self, father_id):
        #Todo: Si le parent etait le pere
        return self.filter(registration__id=father_id)


    def search(self, nip='', firstname='', sex='', birthday='', father='', mother=''):
        r_list = self.all()
        if nip != '':
            nip = r_list.filter(nip=nip)
        if firstname != '':
            firstname = r_list.filter(firstname__icontains=firstname)
        if sex != '':
            r_list = r_list.filter(sex__icontains=sex)
        if birthday != '':
            r_list = r_list.filter(birthday__icontains=birthday)
        if father != '':
            r_list = (
		r_list.filter(registration__lastname__icontains=father__lastname, registration__sex__icontains='M')
            )
        if mother != '':
            r_list = (
                r_list.filter(registration__lastname__icontains=mother__lastname, registration__sex__icontains='F') 
            )

        #if search_fields.get('mairie', ''):
        #    r_list = r_list.filter(mairie__id=search_fields['mairie'])
        #if search_fields.get('arrondissement', ''):
        #    r_list = r_list.filter(arrondissement__id=search_fields['arrondissement'])
        return r_list

class BirthEligibleManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(bcduedate__gte=date.today())

class Birth(ModelEntity):
 
	nip		= models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	firstname 	= models.CharField(max_length=30, null=False, verbose_name='Prénom(s)')
	sex 		= models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe')
	birthweight	= models.DecimalField(max_digits=4,  decimal_places=2, verbose_name="Poids à la naissance")
	birthday 	= models.DateField(null=False, verbose_name='Date de naissance')
	birthhour 	= models.TimeField(null=True, verbose_name='Heure de naissance')
	birthtype       = models.CharField(max_length=20, choices=BIRTH_TYPE, verbose_name="Type de naissance",
					default='Simple', null=True, blank=True)
#	city 		=  models.ForeignKey(Mairie, related_name='mairie_birth', verbose_name='Mairie', 
#				on_delete=models.CASCADE, null=True)
	district 	=  models.ForeignKey(Arrondissement,related_name='arrondissement_birth', verbose_name='Arrondissement de naissance', 
				on_delete=models.CASCADE, null=True)
	neighborhood    = models.ForeignKey(Quartier, related_name='neighbor_birth', null=True, blank=True,
				verbose_name='Lieu de naissance', on_delete=models.CASCADE)
	father	 	= models.ForeignKey(Registration, related_name='father', verbose_name='Père',
				on_delete=models.CASCADE, null=False)
	mother	 	= models.ForeignKey(Registration, related_name='mother', verbose_name='Mère', 
				on_delete=models.CASCADE, null=False)
	declarant 	= models.ForeignKey(Registration, related_name='declarant', verbose_name='Déclarant', 
				on_delete=models.CASCADE, null=False)
	social_number 	= models.CharField(max_length=30, null=True, blank=True, verbose_name='numero social', unique=True)
	bcduedate	= models.DateField(default=(date.today() + timedelta(days=21)), verbose_name="Date d\'échéance", null=True, blank=True)
	created 	= models.DateField(auto_now_add=True)


	objects = BirthManager()
	eligible = BirthEligibleManager()
	
#	def is_late(self):
#		return (self.bcduedate >= date.today())

	def clean(self):
		self.firstname = self.firstname.strip().capitalize()
		super(Birth, self).clean()
		#super(Birth, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.full_clean()
		super(Birth, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('gestciv:birth_update', kwargs={'pk': self.pk})

	def __str__(self):
		return self.firstname 

	class Meta:
		ordering = ['-created']
		verbose_name= ("Naissance")
		verbose_name_plural = ("Naissances")

######################################################################
#
# Adoption: Cette table permet de constituer par l'officier administratif
#	l'acte de naissance du nouveau né.
#	L'officier traitant reçoit les informations nécessaires de la 
#	table BirthDeclaration
#######################################################################
class AdoptionManager(models.Manager):

    #def has_father(self):
    #    return self.filter(registration__nip=self.nip)


    def search(self, nip='', father='', mother='', adoptioncountry='', adoptiondistrict=''):
        r_list = self.all()
        if nip != '':
            nip = r_list.filter(nip=nip)
        if father != '':
            father = r_list.filter(father__lastname__icontains=father__lastname, father__firstname__icontains=father__lastname)
        if mother != '':
            mother = r_list.filter(mother__lastname__icontains=mother__lastname, mother__firstname__icontains=mother__lastname)
        if adoptioncountry != '':
            r_list = r_list.filter(adoptioncountry__icontains=adoptioncountry)
        if adoptiondistrict != '':
            r_list = r_list.filter(adoptiondistrict__icontains=adoptiondistrict)

        return r_list

class Adoption(ModelEntity):
 
	nip		= models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	father		= models.ForeignKey(Registration, related_name='father_adoption', verbose_name='Père adoptif',
				on_delete=models.CASCADE, null=False)
	mother      	= models.ForeignKey(Registration, related_name='mother_adoption', verbose_name='Mère adoptive',
				on_delete=models.CASCADE, null=False)
	adoptioncountry	=  models.ForeignKey(Mairie, related_name='mairie_adoption', verbose_name='Mairie d\'adoption', 
				on_delete=models.CASCADE, null=True)
	adoptiondistrict =  models.ForeignKey(Arrondissement, related_name='arrondissement_adoption', verbose_name='Arrondissement d\'adoption', 
		on_delete=models.CASCADE, null=True)


	objects = AdoptionManager()

	
	def clean(self):
		super(Adoption, self).clean()

	def save(self, *args, **kwargs):
		self.full_clean()
		super(Adoption, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('gestciv:adoption_update', kwargs={'pk': self.pk})

	def __str__(self):
		return self.nip 

	class Meta:
		ordering = ['-created_on']
		verbose_name= ("Adoption")
		verbose_name_plural = ("Adoptions")


######################################################################
#
# BirthCertificate: Cette table permet de constituer par l'officier administratif
#	l'acte de naissance du nouveau né.
#	L'officier traitant reçoit les informations nécessaires de la 
#	table BirthDeclaration
#######################################################################
class BirthCertificateManager(models.Manager):

    def list_childs_by_fathe(self, father_id):
        #Todo: Si le parent etait le pere
        return self.filter(registration__id=father_id)


    def search(self, firstname='', sex='', birthday='', father='', mother=''):
        r_list = self.all()
        if firstname != '':
            firstname = r_list.filter(firstname__icontains=firstname)
        if sex != '':
            r_list = r_list.filter(sex__icontains=sex)
        if birthday != '':
            r_list = r_list.filter(birthday__icontains=birthday)
        if father != '':
            r_list = (
		r_list.filter(registration__lastname__icontains=father__lastname, registration__sex__icontains='M')
            )
        if mother != '':
            r_list = (
                r_list.filter(registration__lastname__icontains=mother__lastname, registration__sex__icontains='F') 
            )

        return r_list


class BirthCertificate(ModelEntity):
 
	nip		= models.CharField(max_length=30, null=True, blank=True, verbose_name='Numéro identifiant privé')
	firstname 	= models.CharField(max_length=30, null=False, verbose_name='Prénom(s)')
	sex 		= models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe')
	birthweight	= models.DecimalField(max_digits=4,  decimal_places=2, verbose_name="Poids à la naissance")
	birthday 	= models.DateField(null=False, verbose_name='Date de naissance')
	birthhour 	= models.TimeField(null=True, verbose_name='Heure de naissance')
	birthcountry	= CountryField(verbose_name=_("Pays de naissance"), default="BJ")
	#birthcountry 	= models.CharField(max_length=50, verbose_name='Pays de naissance', default='Bénin')
	city 		=  models.ForeignKey(Mairie, related_name='mairie_birthcertif', verbose_name='Mairie', 
				on_delete=models.CASCADE, null=True)
	father	 	= models.ForeignKey(Registration, related_name='fathercertif', verbose_name='Father',
				on_delete=models.CASCADE, null=False)
	mother	 	= models.ForeignKey(Registration, related_name='mothercertif', verbose_name='Mère', 
				on_delete=models.CASCADE, null=False)
	declarant 	= models.ForeignKey(Registration, related_name='declarantcertif', verbose_name='Déclarant', 
				on_delete=models.CASCADE, null=False)
	bcduedate	= models.DateField(default=(date.today() + timedelta(days=21)), verbose_name="Date d\'échéance", null=True, blank=True)


	objects = BirthCertificateManager()

	

	def clean(self):
		self.firstname = self.firstname.strip().capitalize()
		super(BirthCertificate, self).clean()

	def save(self, *args, **kwargs):
		self.full_clean()
		self.nip = self.get_nip()
		super(BirthCertificate, self).save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse('gestciv:birth_update', kwargs={'pk': self.pk})
	

	def __str__(self):
		return self.firstname 

	class Meta:
		ordering = ['-bcduedate']
		verbose_name= ("Certificat de naissance")
		verbose_name_plural = ("Certificats de naissances")

class Wedding(ModelEntity):

	husband			= models.ForeignKey(Registration, related_name='husband_wedding', verbose_name='Husband',
					on_delete=models.CASCADE, null=False)
	wife          		= models.ForeignKey(Registration, related_name='wife_wedding', verbose_name='Wife',
					on_delete=models.CASCADE, null=False)
	weddingplace        	= models.DateField(null=False, verbose_name='Lieu de mariage')
	weddingday        	= models.DateField(null=False, verbose_name='Date de mariage')
	recordingday        	= models.DateField(null=False, verbose_name='Date d\enregistrement ')
	certificate_num		= models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Certificat de mariage")


class Divorced(ModelEntity):

	husband			= models.ForeignKey(Registration, related_name='husband_divorced', verbose_name='Husband',
					 on_delete=models.CASCADE, null=False)
	wife          		= models.ForeignKey(Registration, related_name='wife_divorced', verbose_name='Wife',
					 on_delete=models.CASCADE, null=False)
	weddingplace        	= models.DateField(null=False, verbose_name='Lieu de mariage')
	weddingday        	= models.DateField(null=False, verbose_name='Date de mariage')
	recordingday        	= models.DateField(null=False, verbose_name='Date d\'enregistrement ')
	certificate_num		= models.DecimalField(max_digits=10,decimal_places=0, verbose_name="Certificat de mariage")
	num_depend_child	= models.DecimalField(max_digits=2,decimal_places=0, verbose_name="Nombre d\'enfants à charge")


class Separation(ModelEntity):

	husband			= models.ForeignKey(Registration, related_name='husband_separation', verbose_name='Husband',
					 on_delete=models.CASCADE, null=False)
	wife          		= models.ForeignKey(Registration, related_name='wife_separation', verbose_name='Wife',
					 on_delete=models.CASCADE, null=False)
	separationplace        	= models.DateField(null=False, verbose_name='Lieu de séparation')
	separationday        	= models.DateField(null=False, verbose_name='Date de séparation')
	recordingday        	= models.DateField(null=False, verbose_name='Date d\enregistrement ')
	certifier       	= models.ForeignKey(DjangoUser, related_name='certifier_separation' ,
                               		 verbose_name="Autorité agissante", on_delete=models.CASCADE, null=True)

class AppliNewsManager(models.Manager):
    def list(self):
        return self.filter(publish_date__lte=datetime.date.today())

    def get_last(self):
      # We use first, because of the default ordering
        return self.filter(publish_date__lte=datetime.date.today()).first()


class AppliNews(models.Model):
    publish_date = models.DateField(verbose_name=u"Date de publication")
    news = models.TextField(verbose_name=u"Info")

    objects = AppliNewsManager()

    def __str__(self):
        return "%s - %s" % (self.publish_date, self.news)

    class Meta:
        verbose_name = _("Software news (item)")
        verbose_name_plural = _("Software news")
        ordering = ['-publish_date']


def get_nip(self):

	 #################################################################
	 # MAJ du nip/birthnum                                           #
	 #################################################################
	#Homme = 1 / Femme = 2
	sex_number = []
	if self.sex == 'M' :
		sex_number = 1
	elif self.sex == 'F' :
		sex_number = 2

	#Récupère année de naissance
	birthyear_temp = str(self.birthday.year)
	birthyear_temp2 = str(birthyear_temp.split(" "))
	birthyear = birthyear_temp2[4] + birthyear_temp2[5]

	#Récupère mois de naissance
	birthmonth_temp = self.birthday.month
	if len(str(birthmonth_temp)) == 1 :
		birthmonth = '0' + str(birthmonth_temp)
	else :
		birthmonth = birthmonth_temp
		# #Récupère première lettre prénom
		firstname = self.mother.firstname[0]
		#Récupère N° Mairie (ici récupère nom mais sera changé en n°)
		birth_mairie = self.mairie.code
		#Génère un nombre aléaloire :
		#Génère un nombre aléaloire :
		key_temp = randint(0,999999)
		if len(str(key_temp)) == 1 :
			key = '00000' + str(key_temp)
		elif len(str(key_temp)) == 2 :
			key = '0000' + str(key_temp)
		elif len(str(key_temp)) == 3 :
			key = '000' + str(key_temp)
		elif len(str(key_temp)) == 4 :
			key = '00' + str(key_temp)
		elif len(str(key_temp)) == 5 :
			key = '0' + str(key_temp)
		else :
			key = key_temp

			nip = str(birthyear) + \
				str(birthmonth) + \
					str(birth_mairie) + \
						str(lastname) + \
							str(firstname) + \
								str(sex_number)+\
									str(key)

		return nip
