import datetime
from django import forms
#from uni_form.helpers import Layout, Fieldset
#from uni_form.helpers import FormHelper, Submit
#from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions,  StrictButton,TabHolder, Tab
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
#from bootstrap3_datetime.widgets import DateTimePicker
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.admin.widgets import AdminDateWidget

#from crispy_forms.helper import FormHelper
#from crispy_forms.bootstrap import StrictButton
from bootstrap3_datetime.widgets import DateTimePicker

from django.forms.fields import DateField
from gestciv.models import (Registration, Birth, BirthDeclaration, BirthCertificate, Death)
from geodivision.models import (Mairie, Departement, Mairie, Arrondissement, Quartier)
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext_lazy as _


_css_class_required_field = 'required'
_l_default_exclude_fields = ['created_by', 'bcduedate']


SEX_CHOICES=(
        ('M','Masculin'),
        ('F', 'Féminin')
        )


class CommonForm(forms.ModelForm):
    required_css_class = 'required'


class DepartementForm(CommonForm):
	class Meta:
		model = Departement
		fields = ('c_dep', 'nom')


class RegistrationForm(CommonForm):


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Tu modifies le label de la date de naissance pour rajouter le format
		self.fields['birthday'].label = "%s (JJ/MM/AAAA)" % "Date de naissance"
		self.fields['city'].label = "%s (de residence)" % "Mairie"
		#self.fields['district'].label = "%s (de résidence)" % "Arrondissement"
		#self.helper = FormHelper()
		#self.helper.form_class = 'form-horizontal'
		#self.helper.form_id = 'registration-form'

	def clean(self):
		cleaned_data = super().clean()

		homonyms = Registration.objects.filter(
		    firstname__iexact=cleaned_data.get("firstname")
		).filter(
		    lastname__iexact=cleaned_data.get("lastname")
		).filter(
		    birthday=cleaned_data.get("birthday")
		)
		
		if homonyms.exists():
		    self.add_error('lastname', _("This person already exists."))	

	def save(self, *args, **kwargs):
		obj = super(RegistrationForm, self).save(commit=False)
		if obj.title == 'M.':
			obj.sex = 'M'
		elif obj.title == 'Mme':
			obj.sex = 'F'
		obj.save()
		return obj


	class Meta:
		model = Registration
		fields = ('title', 'lastname', 'young_girl_lastname', 'firstname','status','sex',
				'neighborhood','nationality', 'job', 'city','district', 'street_type','ice', 
				'father_name', 'mother_name','ethnie','comp_1','comp_2','phone', 'mail', 'created_by')

	birthday = forms.DateField(
		label=Meta.model._meta.get_field('birthday').verbose_name,
		initial=datetime.date.today()
	    )
	arrived_date = forms.DateField(
		label=Meta.model._meta.get_field('arrived_date').verbose_name,
		initial=datetime.date.today()
	    )


	widgets = {'nationality': CountrySelectWidget()}



class RegistrationSearchForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = ('lastname',)

class CustomLabelModelChoiceField(forms.ModelChoiceField):

	def __init__(self, *args, **kwargs):
		self._label_from_instance = kwargs.pop('label_func')
		super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)

	def label_from_instance(self, obj):
		return self._label_from_instance(obj)

class DeathForm(CommonForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Tu modifies le label de la date de naissance pour rajouter le format
		self.fields['deathday'].label = "%s (JJ/MM/AAAA)" % "Date de décès"

	def clean(self):
		cleaned_data = super().clean()

		homonyms = Death.objects.filter(
			firstname__iexact=cleaned_data.get("firstname")
			).filter(
				lastname__iexact=cleaned_data.get("lastname")
					).filter(
						birthday=cleaned_data.get("birthday")
						)

		if homonyms.exists():
			self.add_error('lastname', _("This person already exists."))

	class Meta:
		model = Death
		fields = ('person', 'eventlocation', 'reglocation', 'cause','deathday','certifier')

		widgets = {
				'birthday': DateTimePicker(
					options={"format": "DD/MM/YYYY", "pickTime": False,
					"useStrict": True, "viewMode": "years",
					"startDate": "01/01/1900"},
					attrs={'placeholder': 'ex: 05/11/1975'}
					),
				'arrived_date': DateTimePicker(
					options={"format": "DD/MM/YYYY", "pickTime": False,
					"useStrict": True, "viewMode": "years",
					"startDate": "01/01/1900"},
					attrs={'placeholder': 'ex: 05/11/1975'}
					)
				}



class BirthDeclarationForm(CommonForm):

	class Meta:
		model = BirthDeclaration
		exclude = _l_default_exclude_fields + ['can_be_issued', 'mairie','nip']
	sex 		= forms.ChoiceField(widget = forms.RadioSelect,choices= SEX_CHOICES)
	bcduedate 	= forms.DateField(label=Meta.model._meta.get_field('bcduedate').verbose_name,
					initial=(datetime.date.today() + datetime.timedelta(days=21)))
	birthday 	= forms.DateField(label=Meta.model._meta.get_field('birthday').verbose_name, initial=datetime.date.today())

	mother =  AutoCompleteSelectField('mother_list', label=Meta.model._meta.get_field('mother').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})


	widgets = {
		'birthday': DatePickerInput(
		       options={"format": "DD/MM/YYYY", "pickTime": False,
		       "useStrict": True, "viewMode": "years",
		       "startDate": "01/01/1900"},
		       attrs={'placeholder': 'ex: 05/11/1975'}
		       )
		}


	def clean(self):
		cleaned_data = super().clean()



class BirthDeclarationSearchForm(CommonForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	class Meta:
		model = BirthDeclaration
		fields = ('nip',)


class BirthForm(CommonForm):

	class Meta:
		model = Birth
		exclude = ['social_number', 'created']


	sex             = forms.ChoiceField(widget = forms.RadioSelect,choices= SEX_CHOICES)

	birthday = forms.DateField(label=Meta.model._meta.get_field('birthday').verbose_name, initial=datetime.date.today())

	firstname = forms.CharField(label=Meta.model._meta.get_field('firstname').verbose_name,
		widget = forms.TextInput(attrs={'size': '50'}))

	father = AutoCompleteSelectField('father_list', label=Meta.model._meta.get_field('father').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	mother =  AutoCompleteSelectField('mother_list', label=Meta.model._meta.get_field('mother').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	declarant =  AutoCompleteSelectField('declarant_list', label=Meta.model._meta.get_field('declarant').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	widgets = {
                'birthday': DatePickerInput(
                       options={"format": "DD/MM/YYYY", "pickTime": False,
                       "useStrict": True, "viewMode": "years",
                       "startDate": "01/01/1900"},
                       attrs={'placeholder': 'ex: 05/11/1975'}
                       )
                }

	def clean(self):
		cleaned_data = super().clean()
		father_lastname = cleaned_data.get("father").lastname
		homonyms = Birth.objects.filter(
			firstname__iexact=cleaned_data.get("firstname")
			).filter(
				father__lastname__iexact=cleaned_data.get(father_lastname)
			).filter(
				birthday=cleaned_data.get("birthday")
			).exclude(
			id=self.instance.id
			)
		if homonyms.exists():
			self.add_error('firstname', _("This person already exists."))

		mother_lastname = cleaned_data.get("mother").lastname
		homonyms = Birth.objects.filter(
			firstname__iexact=cleaned_data.get("firstname")
				).filter(
					father__lastname__iexact=cleaned_data.get(father_lastname)
		).filter(
			birthday=cleaned_data.get("birthday")
				).exclude(
					id=self.instance.id
					)
		if homonyms.exists():
			self.add_error('firstname', _("This person already exists."))



class BirthSearchForm(CommonForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Override the fields making it NOT mandatory
		self.fields['nip'].required = False

		#reader_enabled = forms.BooleanField(label=_("Readers enabled"), initial=True, required=False)

	class Meta:
		model = Birth
		fields = ('nip',)



##################################################################################"""

class BirthCertificateForm(forms.ModelForm):
	fk_parent1 = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Père", 
		label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number), empty_label=None)
	fk_parent2 = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Mère", 
		label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number), empty_label=None)
	lastname = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Nom", 
		label_func=lambda obj: '%s' % (obj.lastname), empty_label=None)
	firstname = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Prénom", 
		label_func=lambda obj: '%s' % (obj.firstname), empty_label=None)
	birthday = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Date de Naissance", 
		label_func=lambda obj: '%s' % (obj.birthday), empty_label=None)
	birthcity = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Ville de Naissance", 
		label_func=lambda obj: '%s' % (obj.birthcity), empty_label=None)
	sex = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Sexe", 
		label_func=lambda obj: '%s' % (obj.sex), empty_label=None)
	birthcountry = CustomLabelModelChoiceField(Registration.objects.filter(), required=False, label = "Pays de Naissance", 
		label_func=lambda obj: '%s' % (obj.birthcountry), empty_label=None)
	mairie = forms.CharField(widget=forms.HiddenInput())
	social_number = CustomLabelModelChoiceField(Registration.objects.filter(),required=False, label = "Numéro Unique", 
		label_func=lambda obj: '%s' % (obj.social_number), empty_label=None)

 
	class Meta :
		model = BirthCertificate
		fields = ['lastname', 'firstname', 'sex', 'birthday', 'birthhour', 'birthcity', 'birthcountry','fk_parent1', 
			'fk_parent2', 'city', 'social_number']
		widgets = {'country': CountrySelectWidget()}

	def __init__(self, *args, **kwargs):   
		super(BirthCertificateForm, self).__init__(*args, **kwargs)
		self.mairie = Mairie.get_default_mairie()			
		for key, value in self.fields.items() :
			self.fields[key].widget.attrs.update({'class':'form-fields'})  
 
class AdoptionForm(CommonForm):

	class Meta:
		model = Birth
		exclude = ['created']



	firstname = forms.CharField(label=Meta.model._meta.get_field('firstname').verbose_name,
		widget = forms.TextInput(attrs={'size': '50'}))

	father = AutoCompleteSelectField('father_list', label=Meta.model._meta.get_field('father').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	mother =  AutoCompleteSelectField('mother_list', label=Meta.model._meta.get_field('mother').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	declarant =  AutoCompleteSelectField('declarant_list', label=Meta.model._meta.get_field('declarant').verbose_name,
		required=False, help_text=None, plugin_options={'autofocus': True, 'minlength': 3})

	widgets = {
                'birthday': DatePickerInput(
                       options={"format": "DD/MM/YYYY", "pickTime": False,
                       "useStrict": True, "viewMode": "years",
                       "startDate": "01/01/1900"},
                       attrs={'placeholder': 'ex: 05/11/1975'}
                       )
                }

	def clean(self):
		cleaned_data = super().clean()
		father_lastname = cleaned_data.get("father").lastname
		homonyms = Birth.objects.filter(
			firstname__iexact=cleaned_data.get("firstname")
			).filter(
				father__lastname__iexact=cleaned_data.get(father_lastname)
			).filter(
				birthday=cleaned_data.get("birthday")
			).exclude(
			id=self.instance.id
			)
		if homonyms.exists():
			self.add_error('firstname', _("This person already exists."))

		mother_lastname = cleaned_data.get("mother").lastname
		homonyms = Birth.objects.filter(
			firstname__iexact=cleaned_data.get("firstname")
				).filter(
					father__lastname__iexact=cleaned_data.get(father_lastname)
		).filter(
			birthday=cleaned_data.get("birthday")
				).exclude(
					id=self.instance.id
					)
		if homonyms.exists():
			self.add_error('firstname', _("This person already exists."))



class BirthSearchForm(CommonForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Override the fields making it NOT mandatory
		self.fields['nip'].required = False

		#reader_enabled = forms.BooleanField(label=_("Readers enabled"), initial=True, required=False)

	class Meta:
		model = Birth
		fields = ('nip',)
 
class IdentityForm(forms.ModelForm) :
     
    class Meta :
        model = Registration
        fields = ['title', 'lastname', 'firstname', 'sex', 'birthday', 'nationality',
		'job', 'street_type', 'city', 'phone']
        widgets = {'country': CountrySelectWidget()}



class StatisticsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_year = Registration.objects.order_by('arrived_date').first().arrived_date.year
        year_choices = [(year, year) for year in range(first_year, datetime.date.today().year + 1)]
        self.fields['year'] = forms.IntegerField(
            widget=forms.Select(
                choices=year_choices
            ),
            required=True,
            label=_("Year")
        )
