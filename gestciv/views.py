from __future__ import unicode_literals
import logging
import os
from io import BytesIO
import requests

from datetime import date
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from random import randint
#from django.core.urlresolvers import reverse_lazy
#from formtools.wizard.views import SessionWizardView
from django.template import RequestContext, Context
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from gestciv.models import (Registration, Birth, Language, ReferenceEntity, AppliNews, 
				UserNavigationHistory,  BirthDeclaration, Death)
from geodivision.models import (Mairie, Departement, Mairie, Arrondissement, Quartier)

from gestciv.forms import (RegistrationForm, BirthDeclarationForm, BirthForm, RegistrationSearchForm, 
				BirthSearchForm, BirthDeclarationSearchForm, BirthCertificateForm, 
				DepartementForm, DeathForm, StatisticsForm)
from django.views.generic.detail import DetailView
from django.template.loader import get_template, render_to_string 
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from weasyprint import HTML, CSS
from django.utils.text import slugify
from django.conf import settings
from datetime import date, datetime, timedelta
from django.core.files.base import ContentFile
from django.db.models import Q

from django_weasyprint import WeasyTemplateResponseMixin

#import pdfkit
import logging


#from djappypod.response import OdtTemplateResponse

logger = logging.getLogger(__name__)
PAGINATION_SIZE = 15

def load_user_nav_history(request, user):
    lst = UserNavigationHistory.objects.get_list(user)
    user_nav_list = []
    for user_nav in lst:
        user_nav_list.append((user_nav.url, user_nav.title))
    request.session['user_nav_list'] = user_nav_list


def clear_user_nav_history(request):
    request.session['user_nav_list'] = None


class ProtectedView(object):
    login_url = reverse_lazy('gestciv:login')

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProtectedView, cls).as_view(**initkwargs)
        return login_required(view, login_url=cls.login_url)

class LogoutView(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        clear_user_nav_history(request)
        return HttpResponseRedirect(reverse('gestciv:login'))

class LoginView(TemplateView):

    template_name = 'gestciv/login.html'
    logging_error_msg = _("Login error - wrong username or password.")

    def login_error(self):
        messages.error(self.request, self.logging_error_msg)
        return HttpResponseRedirect(reverse('gestciv:login'))

    def post(self, request):
        """Gather the username and password provided by the user.
        This information is obtained from the login form.
        """


        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the credentials are correct.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                load_user_nav_history(request, user)
                return HttpResponseRedirect(reverse('gestciv:home'))
            else:
                # An inactive account was used - no logging in!
                messages.error(self.request, self.logging_error_msg)
                return self.login_error()
        else:
            # Bad login details were provided. So we can't log the user in.
            return self.login_error()



class HomeView(ProtectedView, TemplateView):
	template_name = 'gestciv/index.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['last_birth_list'] = BirthDeclaration.objects.all()[:10]
		context['last_appli_news_list'] = AppliNews.objects.all()[:3]
		context['default_mairie'] = Mairie.get_default_mairie()
		context['brothers_list'] = BirthDeclaration.objects.list_brothers_by_mother(1)
		return context


class EntityCreateView(ProtectedView, CreateView):
	def form_invalid(self, form, error_msg="Erreur lors de la sauvegarde."):
		messages.error(self.request, form.errors.as_data())
		return self.render(self.get_context_data(form=form))
		#return super(EntityCreateView, self).form_invalid(form)

	def form_valid(self, form, success_msg="Enregistrement réussi."):
		form.instance.created_by = self.request.user
		messages.success(self.request, success_msg)
		return super(EntityCreateView, self).form_valid(form)


class EntityUpdateView(ProtectedView, UpdateView):
    def get(self, request, **kwargs):
        ret = super(EntityUpdateView, self).get(request, kwargs)
        if not UserNavigationHistory.exist_url(request.path):
            UserNavigationHistory.add(request.path, self.object._meta.verbose_name + " : " + str(self.object),
                                      self.request.user)
            load_user_nav_history(self.request, self.request.user)
        return ret

    def form_invalid(self, form, error_msg=_("Error when saving the record.")):
        messages.error(self.request, error_msg)
        return super(EntityUpdateView, self).form_invalid(form)

    def form_valid(self, form, success_msg=_("Record successful saved.")):
        form.instance.modified_by = self.request.user
        messages.success(self.request, success_msg)
        return super(EntityUpdateView, self).form_valid(form)


class EntityListView(ProtectedView, ListView):
    object_list = None

    def _build_query(self, search_fields):
        # Abstract method
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # The method of the super class will put 'object_list' and a 'paginator' and 'page_obj' objects in the context
        # of the template
        context = super(EntityListView, self).get_context_data(**kwargs)
        cur_page_nb = context['page_obj'].number
        num_pages = context['paginator'].num_pages

        pages_window = [i for i in range(max(cur_page_nb-3, 1), min(cur_page_nb+4, num_pages + 1))]
        context['pages_window'] = pages_window
        context['window_first_page_nb'] = pages_window[0]
        context['window_last_page_nb'] = pages_window[-1]

        if self.form_class is not None:
            context['search_form'] = self.form_class()
        return context

    def get(self, request, **kwargs):
        """
        Warning: this method bypasses the super one
        """
        self.object_list = self.get_queryset()
        order_field = request.GET.get('order_field')
        if request.GET.get('page') is not None or order_field is not None:
            if request.session.get('search_fields') is not None:
                # Rebuild the query upon the search terms entered by the user
                self._build_query(request.session.get('search_fields'))
            else:
                if self.object_list is None:  # Make sure the subclass didn't already create self.object_list
                    self.object_list = self.model.objects.all()
        else:
            # First time we arrive on a list page
            if self.object_list is None:  # Make sure the subclass didn't already create self.object_list
                self.object_list = self.model.objects.all()
            request.session['order_field'] = None
            request.session['search_fields'] = None
        if order_field is not None:
            # Sorting request
            if request.session.get('order_field') is not None: # A previous sorting request was done on this page
                # Check if the sorting field changed according to the last sorting request
                stored_field = (
                    request.session.get('order_field')[1:]
                    if request.session.get('order_field').startswith('-') else request.session.get('order_field')
                )
                if order_field == stored_field:
                    # Invert sort order
                    if request.session.get('order_field').startswith('-'):
                        request.session['order_field'] = request.session.get('order_field')[1:]
                    else:
                        request.session['order_field'] = '-' + request.session.get('order_field')
                else:
                    # Sorting request on a new field
                    request.session['order_field'] = order_field
            else:
                # First time sorting request for this page
                request.session['order_field'] = order_field
        if request.session.get('order_field') is not None:
            self.object_list = self.object_list.order_by(request.session.get('order_field'))

        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request):
        self._build_query(request.POST)
        request.session['search_fields'] = request.POST
        request.session['order_field'] = None
        context = self.get_context_data()
        if self.form_class is not None:
            context['search_form'] = self.form_class(request.POST)
        return self.render_to_response(context)



class EntityDeleteView(ProtectedView, DeleteView):
    pass



class  DepCreateView(EntityCreateView):
        template_name = 'gestciv/dept_detail.html'
        model = Departement
        form_class = DepartementForm  


class RegistrationCreateView(EntityCreateView):
	template_name = 'gestciv/registration_detail.html'
	model = Registration
	form_class = RegistrationForm

	def get_success_url(self):
		
#		form.instance.created_by = self.request.user
		# We created the person from the birth page
		if self.kwargs.get('father_redirect_to_birth', None) is not None:
			birth_post = self.request.session['birth_post_form']
			birth_post['father'].append(str(self.object.id))
			self.request.session['birth_post_form'] = birth_post
			return reverse('gestciv:birth_add', args=['from_external_page'])

		if self.kwargs.get('mother_redirect_to_birth', None) is not None:
			birth_post = self.request.session['birth_post_form']
			birth_post['mother'].append(str(self.object.id))
			self.request.session['birth_post_form'] = birth_post
			return reverse('gestciv:birth_add', args=['from_external_page'])

		return super().get_success_url()

	def get_context_data(self, **kwargs):

		# Call the base implementation first to get a context
		context = super(RegistrationCreateView, self).get_context_data(**kwargs)
		registration_form = context.get('form')
		#birthdeclare_form.initial['language'] = Language.get_default_language()
		registration_form.initial['city'] = Mairie.get_default_mairie()
		registration_form.initial['created_by'] = self.request.user
		registration_form.initial['modified_by'] = self.request.user
		registration_form.initial['created_on'] = datetime.today()
		registration_form.initial['sex'] = 'M'

#		 birth_form.fields['birthhour'].widget.attrs['readonly'] = True
		context = {"form": registration_form, }
		return context

	def form_valid(self, form):
		form.instance.sex = 'M'
		if form.instance.title == 'M.':
			form.instance.sex = 'M'
		elif form.instance.title == 'MMe':
			form.instance.sex = 'F' 
		super(RegistrationCreateView, self).form_valid(form)
		return HttpResponseRedirect(reverse('gestciv:registration_update', args=[form.instance.id]))


class RegistrationUpdateView(EntityUpdateView):
    template_name = 'gestciv/registration_detail.html'
    model = Registration
    form_class = RegistrationForm

    def form_valid(self, form):
        return super(RegistrationUpdateView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RegistrationUpdateView, self).get_context_data(**kwargs)
        #context['birth_list'] = self.object.birth.all()
        return context


class RegistrationDeleteView(EntityDeleteView):
	template_name = 'gestciv/confirm_delete.html'
	model = Registration
	success_url = reverse_lazy('gestciv:registration_list')

	def get(self, request, **kwargs):
		# This method is called before displaying the page 'template_name'
		registration = Registration.objects.get(id=kwargs['pk'])
	#	if registration.birth_set.count() > 0:
	#		messages.error(self.request, _("Unable to remove this registration because it is referenced in a birth."))
	#		return redirect('gestciv:registration_update', pk=author.id)
		#return redirect(author) # Call to get_absolute_url of Author model
		return super(RegistrationDeleteView, self).get(request, kwargs)




class RegistrationListView(EntityListView):
    template_name = 'gestciv/registration_list.html'
    model = Registration
    paginate_by = PAGINATION_SIZE
    form_class = RegistrationSearchForm

    def _build_query(self, search_fields):
        self.object_list = self.model.objects.search(name=search_fields['lastname'])

class BirthDeclarationCreateView(EntityCreateView):
	template_name = 'gestciv/birthdeclaration_detail.html'
	model = BirthDeclaration
	form_class = BirthDeclarationForm

	def get_success_url(self):
		
		if self.kwargs.get('search_for_birth', None) is not None:
			birth_post = self.request.session['birth_post_form']
			birth_post['nip'].append(str(self.object.id))
			birth_post['nip'] = self.object.id

			self.request.session['birth_post_form'] = birth_post
			return reverse('gestciv:birth_add', args=['from_external_page'], new_birth=self.object.id)
		return super().get_success_url()

	def get_context_data(self, **kwargs):
		
		# Call the base implementation first to get a context
		context = super(BirthDeclarationCreateView, self).get_context_data(**kwargs)
		birthdeclare_form = context.get('form')
		#birthdeclare_form.initial['language'] = Language.get_default_language()
		mairie = Mairie.get_default_mairie() 
		arrondissement = Arrondissement.get_arrondissement()

		birthdeclare_form.initial['mairie'] = mairie
		birthdeclare_form.initial['district'] = arrondissement
		birthdeclare_form.initial['created_by'] = self.request.user
		birthdeclare_form.initial['modified_by'] = self.request.user
		birthdeclare_form.initial['created_on'] = datetime.today() 
		birthdeclare_form.initial['midwife'] = self.request.user
		if self.request.user.groups.count() > 0 :
			birthdeclare_form.initial['midwifegroup'] = self.request.user.groups.all()[0]
		
		birthdeclare_form.initial['can_be_issued'] = True
		
		context = {"form": birthdeclare_form, }
		return context

	def form_valid(self, form):

		if self.request.user.groups.count() > 0 :
			form.instance.midwifegroup = self.request.user.groups.all()[0]
		form.instance.created_by = self.request.user
		form.instance.nip = '12345' # Just to bypass the save method
		form.instance.mairie = Mairie.get_default_mairie()
		form.instance.can_be_issued = True

		super(BirthDeclarationCreateView, self).form_valid(form)
		birth_id = self.object.id
		birth_nip = form.instance.nip 

		return HttpResponseRedirect(reverse('gestciv:nbirth_update', args=[birth_id]))



class BirthDeclarationUpdateView(EntityUpdateView):
	template_name = 'gestciv/birthdeclaration_detail.html'
	model = BirthDeclaration
	form_class = BirthDeclarationForm

	def get_context_data(self, **kwargs):
		birth= BirthDeclaration.objects.filter(id=self.kwargs['pk'])[0]

		# Call the base implementation first to get a context
		context = super(BirthDeclarationUpdateView, self).get_context_data(**kwargs)
		context['mairie'] = Mairie.get_default_mairie()
		birth_nip = BirthDeclaration.objects.filter(nip='nip')
		context['nip'] = context.get('nip')
		context['mother'] = BirthDeclaration.objects.filter(mother=self.object.mother)
		context['birth_list'] = birth.mother.new_birth_mother.all().exclude(id=self.kwargs['pk'])
		context['brothers_list'] = BirthDeclaration.objects.list_brothers_by_mother(self.object.mother.id)
		return context

class BirthDeclarationListView(EntityListView):

	template_name = 'gestciv/birthdeclaration_list.html'
	model = BirthDeclaration
	paginate_by = PAGINATION_SIZE
	form_class = BirthDeclarationSearchForm

	#  def get_queryset(self):
	# By default only display enabled readers
	#return super().get_queryset().filter(disabled_on__isnull=True)

	#          return super().get_queryset().filter(can_be_issued=True)

	def _build_query(self, search_fields):
		self.object_list = self.model.objects.search(nip=search_fields['nip'])
#                self.object_list = BirthDeclaration.model.objects.search(nip=(search_fields['nip']))


class DeathCreateView(EntityCreateView):
	template_name = 'gestciv/death_detail.html'
	model = Death
	form_class = DeathForm

	def get_context_data(self, **kwargs):
		
		# Call the base implementation first to get a context
		context = super(DeathCreateView, self).get_context_data(**kwargs)
		death_form = context.get('form')
		death_form.initial['mairie'] = Mairie.get_default_mairie()
		death_form.initial['created_by'] = self.request.user
		death_form.initial['modified_by'] = self.request.user
		death_form.initial['created_on'] = datetime.today() 
		death_form.initial['certifier'] = self.request.user
		death_form.initial['can_be_issued'] = True
		
		context = {"form": death_form, }
		return context

	def form_valid(self, form):

		form.instance.person.death=True

		super(DeathCreateView, self).form_valid(form)
		death_nip = form.instance.nip 

		return HttpResponseRedirect(reverse('gestciv:death_update', args=[death_id]))



class BirthCreateView(EntityCreateView):
	template_name = 'gestciv/birth_detail.html'
	model = Birth
	form_class = BirthForm

	def get_initial(self):
		if 'from_external_page' in self.kwargs and 'birth_post_form' in self.request.session:
		# If we added a birth or a person, we want to restore the initial form
			birth_post_form = self.request.session['birth_post_form']
			del self.request.session['birth_post_form']
			return birth_post_form
		return super().get_initial()


	def get_context_data(self, **kwargs):

		#Call the base implementation first to get a context
		context = super(BirthCreateView, self).get_context_data(**kwargs)
		birth_post = self.request.session['birth_post_form']
		birth_form = context.get('form')
		del self.request.session['birth_post_form']

		context['language'] = Language.get_default_language()

		return context

	def form_valid(self, form):
		super(BirthCreateView, self).form_valid(form)
		birth_id = self.object.id
		return HttpResponseRedirect(reverse('gestciv:birth_update', args=[birth_id]))

class BirthUpdateView(EntityUpdateView):
	template_name = 'gestciv/birth_detail.html'
	model = Birth
	form_class = BirthForm

	def get_context_data(self, **kwargs):

		context = super(BirthUpdateView, self).get_context_data(**kwargs)
		context['mairie'] = Mairie.get_default_mairie()
		birth_id = context.get('id')
		context['father_child_list'] = Birth.objects.filter(father=self.object.father)
		context['mother_child_list'] = Birth.objects.filter(mother=self.object.mother)
		return context

class BirthDeleteView(EntityDeleteView):
	template_name = 'gestciv/confirm_delete.html'
	model = Birth
	success_url = reverse_lazy('gestciv:birth_list')
		
class BirthListView(EntityListView):

	template_name = 'gestciv/birth_list.html'
	model = Birth
	paginate_by = PAGINATION_SIZE
	form_class = BirthSearchForm

	def get_queryset(self):
		return Birth.objects.get_queryset().all()

	def _build_query(self, search_fields):
		self.object_list = Birth.objects.search(nip=(search_fields('nip')))


class BirthDeclarationImportView(ProtectedView, TemplateView):
	template_name = 'gestciv/birth_declaration_import.html'

	def post(self, request):
		cmd = request.POST['cmd']
		if cmd == 'search_birth':
			# Search new birth info
			birth_nb = request.POST['birth_nb']
			birth_meta = None 
			if birth_nb:
				birth_meta = BirthDeclaration.objects.search(nip=birth_nb)[0]
				#birth_meta = self._init_certificate_from_Bd(birth_nb, request)
			if birth_meta:
				logger.debug("BIRTH data: {}".format(birth_meta))
				return self._init_certificate_from_Bd(birth_meta, request)
			else:  # No Declaration found
				return render(
				    request,
				    self.template_name,
				    {
					'search': True,
				    },
				)
		elif cmd == 'import_birth':
			# After submit button to import has been pressed
			mother_id = None
			if request.POST.get('mother_id'):  # The publisher already exists in the DB
				mother_id = Registration.objects.get(id=request.POST['mother_id']).id

		# Initialize the birth with the values that have been entered
		mother_ids = [mother_id] if mother_id is not None else []
		birth_nb =  request.POST.get('nip')
		birth_meta = BirthDeclaration.objects.search(nip=birth_nb)[0]
		birth_form = BirthForm(
		initial={
				'birthday':birth_meta.birthday, 
				'nip': request.POST.get('nip'),
				'sex': request.POST.get('sex'),
				#'birthcountry': birth_meta.birthcountry,
				'district': birth_meta.district,
				'neighborhood': birth_meta.neighborhood,
				'birthweight': birth_meta.birthweight,
				'birthhour':birth_meta.birthhour,
				'city': Mairie.get_default_mairie(),
				'mother': mother_id,

				}
			)
		#birth_form.fields['birthcountry'].widget.attrs['readonly'] = True
		birth_form.fields['birthhour'].widget.attrs['readonly'] = True
		birth_form.fields['birthweight'].widget.attrs['readonly'] = True
		birth_form.fields['birthday'].widget.attrs['readonly'] = True
		birth_form.fields['mother'].widget.attrs['readonly'] = True
		#birth_form.fields['city'].widget.attrs['readonly'] = True
		birth_form.fields['nip'].widget.attrs['readonly'] = True
		birth_form.fields['sex'].widget.attrs['readonly'] = True
		birth_form.fields['district'].widget.attrs['readonly'] = True
		birth_form.fields['neighborhood'].widget.attrs['readonly'] = True
		return render( request, 'gestciv/birth_detail.html', { 'form': birth_form, },)



	def _init_certificate_from_Bd(self, birth_meta, request):
        # Initialize birth certificate form from birth declaration data
		birth = Birth.objects.filter(nip=birth_meta.nip)
		if not birth:  #This declaration already exists on Birth table
			return render(
				request,
				self.template_name,
				{
					'new_birth': birth_meta,
					'search': True,
					'mother': birth_meta.mother,
					'mother_firstname': birth_meta.mother.firstname,
					'mother_lastname': birth_meta.mother.lastname,
					'mother_birthday': birth_meta.mother.birthday,
					'mother_city': birth_meta.mother.city,
					'district': birth_meta.district,
					'neighborhood': birth_meta.neighborhood,
				},)

		else: 
			return render(request,
				self.template_name,
					{
						'birth': birth_meta,
						'search': True,
						},
					)

class DeathDeclarationView(ProtectedView, TemplateView):
	template_name = 'gestciv/death_declaration.html'

	def post(self, request):
		cmd = request.POST['cmd']
		if cmd == 'search_person':
			# Search new birth info
			person_nip = request.POST['person']
			person_meta = None 
			if person_nip:
				person_meta = Registration.objects.search(nip=person_nip)[0]
			if person_meta:
				logger.debug("PERSON data: {}".format(person_meta))
				return self._init_certificate_from_death(person_meta, request)
			else:  # No Declaration found
				return render(
				    request,
				    self.template_name,
				    {
					'search': True,
				    },
				)
		elif cmd == 'import_person':
			# After submit button to import has been pressed
			mother_id = None
			if request.POST.get('mother_id'):  # The publisher already exists in the DB
				mother_id = Registration.objects.get(id=request.POST['mother_id']).id

		# Initialize the birth with the values that have been entered
		mother_ids = [mother_id] if mother_id is not None else []
		birth_nb =  request.POST.get('nip')
		birth_meta = BirthDeclaration.objects.search(nip=birth_nb)[0]
		birth_form = BirthForm(
		initial={
				'birthday':birth_meta.birthday, 
				'nip': request.POST.get('nip'),
				'sex': request.POST.get('sex'),
				'birthcountry': birth_meta.birthcountry,
				'birthweight': birth_meta.birthweight,
				'birthhour':birth_meta.birthhour,
				'city': Mairie.get_default_mairie(),
				'mother': mother_id,

				}
			)
		birth_form.fields['birthcountry'].widget.attrs['readonly'] = True
		birth_form.fields['birthhour'].widget.attrs['readonly'] = True
		birth_form.fields['birthweight'].widget.attrs['readonly'] = True
		birth_form.fields['birthday'].widget.attrs['readonly'] = True
		birth_form.fields['mother'].widget.attrs['readonly'] = True
		#birth_form.fields['city'].widget.attrs['readonly'] = True
		birth_form.fields['nip'].widget.attrs['readonly'] = True
		birth_form.fields['sex'].widget.attrs['readonly'] = True
		return render( request, 'gestciv/birth_detail.html', { 'form': birth_form, },)



	def _init_certificate_from_death(self, person_meta, request):
        # Initialize birth certificate form from birth declaration data
		death = Death.objects.filter(nip=person_meta.nip)
		if death:  #This declaration already exists on Birth table
			return render(
				request,
				self.template_name,
				{
					'new_death': person_meta,
					'search': True,
					'person': death.person,
					'reglocation': death.reglocation,
					'eventlocation': death.eventlocation,
					'cause': death.cause,
					'deathday': death.deathday,
				},)

		else: 
			return render(request,
				self.template_name,
					{
						'death': person_meta,
						'search': True,
						},
					)


def save_father_form_to_session(request, dest_url):
    """
    View called from within the birth page to add either a father or a mother
    """
    birth_post = request.POST.copy()
    birth_post['father'] = [item for item in birth_post['father'].split('|') if item]
    request.session['birth_post_form'] = birth_post
    # dest_url will either contain the url to create an author or the url to create a publisher
    return HttpResponseRedirect(reverse(dest_url, args=['father_redirect_to_birth']))


def save_mother_form_to_session(request, dest_url):
    """
    View called from within the birth page to add either a father or a mother
    """
    birth_post = request.POST.copy()
    birth_post['mother'] = [item for item in birth_post['mother'].split('|') if item]
    request.session['birth_post_form'] = birth_post
    # dest_url will either contain the url to create an author or the url to create a publisher
    return HttpResponseRedirect(reverse(dest_url, args=['mother_redirect_to_birth']))


def search_for_new_birth(request, dest_url):
    """
    View called from within the birth page to search for a new birth in order to create a birth certificate
    """
    birth_post = request.POST.copy()
    birth_post['nip'] = [item for item in birth_post['nip'].split('|') if item]
    request.session['birth_post_form'] = birth_post
    # dest_url will either contain the url to search a new birth 
    return HttpResponseRedirect(reverse(dest_url, args=['search_for_birth']))


def gen_acte_naissance(request, birth_id):
	birth = get_object_or_404(Birth, id=birth_id)
	mairie = Mairie.get_default_mairie()
	current_date = datetime.now()

	folder = date.today().strftime("%B")
	# create the folder if it doesn't exist.
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
	except:
		pass

	html = render_to_string('gestciv/etat_civil.html',
		{'birth': birth, 'mairie':mairie, 'current_date':current_date})
	response = HttpResponse(content_type='application/pdf')
	filename= "birth_{}_{}_{}.pdf".format(birth.firstname,birth.father.lastname,birth.birthday)
	full_filename = os.path.join(settings.MEDIA_ROOT, folder, filename)

	response['Content-Disposition'] ='attachement;filename="{}"'.format(filename)
	#HTML(string=html).write_pdf(response, stylesheets=[CSS(settings.STATIC_PDF + 'pdf.css')])
	pdf_file = HTML(string=html).write_pdf()
	f = open(os.path.join(settings.MEDIA_ROOT, folder, filename), 'wb')
	f.write(pdf_file)
	return response



def gen_possession_etat_pdf(request, registration_id):
	person = get_object_or_404(Registration, id=registration_id)
        #Pas de possession d'état pour un décédé
	if person.status == 'I':
           return render('gestciv:registration_list')

	mairie = Mairie.get_default_mairie()
	cur_quartier = Quartier.objects.filter(cq=request.user)[0]
	article = person.get_article_type()
	type_article = article['article']
	type_terminaison = article['terminaison']
	type_pronom = article['pronom']
	filename="possession_{}{}{}.pdf".format(person.firstname,person.lastname,person.birthday)
	current_date = datetime.now()

	html = render_to_string('gestciv/possession-etat.html',
		{'person': person, 'mairie':mairie, 'quartier': cur_quartier, 'current_date':current_date, 
			'article':type_article, 'terminaison':type_terminaison, 'pronom':type_pronom})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)

	# create the folder if it doesn't exist.
	folder = date.today().strftime("%B")
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
	except:
		pass

	pdf_file = HTML(string=html).write_pdf()
	#f = open(os.path.join(settings.MEDIA_ROOT, folder, filename), 'wb')
	full_filename = os.path.join(settings.MEDIA_ROOT, folder, filename)
	file_object = open(full_filename, 'wb')
	file_object.write(pdf_file)

	return response


def gen_attestation_residence_pdf(request, registration_id):
        person = get_object_or_404(Registration, id=registration_id)
        #Pas d'attestation de residence pour un décédé
        if person.status == 'I':
            success_url = reverse_lazy('gestciv:registration_list')

        mairie = Mairie.get_default_mairie()
        #quartier = Quartier.objects.get(nom=request.user)
        cur_quartier = Quartier.objects.filter(cq=request.user)[0]
        article = person.get_article_type()
        type_article = article['article']
        type_terminaison = article['terminaison']
        type_pronom = article['pronom']
        #cur_arrondissement = Arrondissement.objects.filter(nom=cur_quartier.cq)
        current_date = datetime.now()

        filename="residence_{}{}{}.pdf".format(person.firstname,person.lastname,person.birthday)
        html = render_to_string('gestciv/template_attestation_residence.html',
                {'person': person, 'mairie':mairie, 'quartier': cur_quartier, 'current_date':current_date,
                        'article':type_article, 'terminaison':type_terminaison, 'pronom':type_pronom})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = filename="{}".format(filename)

        
        # create the folder if it doesn't exist.
        folder = date.today().strftime("%B")
        try:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
        except:
            pass

        pdf_file = HTML(string=html).write_pdf()
        f = open(os.path.join(settings.MEDIA_ROOT, folder, filename), 'wb')
        return response

@login_required
def BirthFormUniqueNumber(request, pk) :
     
	#User fill some fields
	new_birth = BirthDeclaration.objects.get(pk=pk)
     
	if request.method == 'POST':
		form = BirthUpdateForm(request.POST or None)
		if form.is_valid() :   # Vérification sur la validité des données
			post = form.save()
			return HttpResponseRedirect(reverse('gestciv:birth_update', kwargs={'nip': new_birth.nip}))
 
	else:
 
		birth_id = context.get('id')
		context['nip'] = new_birth.nip
		context['sex'] = new_birth.sex
		context['birthweight'] = new_birth.birthweight
		context['birthhour'] = new_birth.birthhour
		context['country'] = new_birth.birthcountry
		context['city'] = new_birth.birthcity
		context['mother'] = new_birth.mother

	return render(request, 'gestciv:birth_update', context)

class StatisticsView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = StatisticsForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = StatisticsForm(request.POST)
        if search_form.is_valid():
            context['statistics'] = self.get_stats(search_form.cleaned_data['year'])

        context['search_form'] = search_form

        return self.render_to_response(context)


class StatisticsRegistrationView(StatisticsView):
    age_slices = {
        '0_14': {'label': _('0-14 years'), 'count': 0, 'percent': 0,
                 'gender': {'m': {'count': 0, 'percent': 0}, 'f': {'count': 0, 'percent': 0}},
                 'resident': {'count': 0, 'percent': 0},
                 'non_resident': {'count': 0, 'percent': 0},
                 'born_after': (lambda year: date(year-14, 1, 1))},
        '15_24': {'label': _('15-24 years'), 'count': 0, 'percent': 0,
                  'gender': {'m': {'count': 0, 'percent': 0}, 'f': {'count': 0, 'percent': 0}},
                  'resident': {'count': 0, 'percent': 0},
                  'non_resident': {'count': 0, 'percent': 0},
                  'born_after': (lambda year: date(year-24, 1, 1)),
                  'born_before': (lambda year: date(year-15, 12, 31))},
        '25_64': {'label': _('25-64 years'), 'count': 0, 'percent': 0,
                  'gender': {'m': {'count': 0, 'percent': 0}, 'f': {'count': 0, 'percent': 0}},
                  'resident': {'count': 0, 'percent': 0},
                  'non_resident': {'count': 0, 'percent': 0},
                  'born_after': (lambda year: date(year-64, 1, 1)),
                  'born_before': (lambda year: date(year-25, 12, 31))},
        '65_over': {'label': _('Over 65 years'), 'count': 0, 'percent': 0,
                    'gender': {'m': {'count': 0, 'percent': 0}, 'f': {'count': 0, 'percent': 0}},
                    'resident': {'count': 0, 'percent': 0},
                    'non_resident': {'count': 0, 'percent': 0},
                    'born_before': (lambda year: date(year-65, 12, 31))},
    }

    def get_stats(self, year):
        born_before = datetime(year, 12, 31, 23, 59, 59)
        statistics = {
            'total_num_births': BirthDeclaration.objects.all(),
            'total_num_declared_birth': Birth.objects.all(),
            'category': {},
        }

        for category in Birth.objects.all():
            statistics['category'][category.sex] = {
                'label': category.sex,
                'origins': {
                    'all': {
                        'total': {
                            'count': Birth.objects.filter(created_on__lte=acquired_before, sex=category.sex).count()
                        },
                        'audiences': OrderedDict()
                    },
                    'items': OrderedDict()
                },
            }

            for audience in Arrondissement.objects.all():
                statistics['category'][category.label]['origins']['all']['audiences'][audience.label] = {
                    'count': Book.objects.filter(bookcopy__registered_on__lte=acquired_before,
                                                 bookcopy__disabled_on__isnull=True,
                                                 category=category, audiences=audience).count()
                }
            content = {}
            for origin in BookCopyOrigin.objects.all():
                content[origin.label] = {
                    'total': {
                        'count': Book.objects.filter(bookcopy__registered_on__lte=acquired_before,
                                                     bookcopy__disabled_on__isnull=True,
                                                     category=category, bookcopy__origin=origin).count()
                    },
                    'audiences': {}
                }
                for audience in BookAudience.objects.all():
                    content[origin.label]['audiences'][audience.label] = {
                        'count': Book.objects.filter(bookcopy__registered_on__lte=acquired_before,
                                                     bookcopy__disabled_on__isnull=True,
                                                     category=category, audiences=audience,
                                                     bookcopy__origin=origin).count()
                    }
            statistics['category'][category.label]['origins']['items'].update(content)
        return statistics




class StatisticsBirthView(StatisticsRegistrationView):
	template_name = 'gestciv/statistics_birth.html'

	@staticmethod
	def get_number_of_births_by_gender(max_create_date, gender, born_after=None, born_before=None):
		qs = Birth.eligible.filter(created_on__lte=max_create_date, sex__iexact=gender)
		if born_after is not None:
			qs = qs.filter(birthday__gte=born_after)
		if born_before is not None:
			qs = qs.filter(birthday__lte=born_before)
		return qs.count()

	@staticmethod
	def get_number_of_birth_by_district(max_create_date, districts, born_after=None, born_before=None):
		for district in districts: 
			qs = Birth.eligible.filter(created_on__lte=max_create_date, district__iexact=district)
			if born_after is not None:
			    qs = qs.filter(birthday__gte=born_after)
			if born_before is not None:
			    qs = qs.filter(birthday__lte=born_before)
			return qs.count()

	@staticmethod
	def calculate_age_slices_stats(statistics, year):
		# Reader cities are always in upper case (it avoids query problems with accents)
		mairie=Mairie.objects.filter(Q(is_default = True))
		birth_arrondissement = Arrondissement.objects.filter(mairie=mairie[0])
		#library_city = GeneralConfiguration.objects.first().library_city.upper()
		max_inscription_date = date(year, 12, 31)
		statistics['year'] = year

		# Statistics by gender
		for gender in ('f', 'm'):
			born_after = statistics['age_slices']['0_14']['born_after'](year)
			statistics['age_slices']['0_14']['gender'][gender]['count'] = (
				StatisticsBirthView.get_number_of_births_by_gender(max_inscription_date, gender, born_after)
				)

			born_after = statistics['age_slices']['15_24']['born_after'](year)
			born_before = statistics['age_slices']['15_24']['born_before'](year)
			statistics['age_slices']['15_24']['gender'][gender]['count'] = (
				StatisticsBirthView.get_number_of_births_by_gender(max_inscription_date, gender,
				born_after, born_before)
				)

			born_after = statistics['age_slices']['25_64']['born_after'](year)
			born_before = statistics['age_slices']['25_64']['born_before'](year)
			statistics['age_slices']['25_64']['gender'][gender]['count'] = (
				StatisticsBirthView.get_number_of_births_by_gender(max_inscription_date, gender,
					born_after, born_before)
			    )
			born_before = statistics['age_slices']['65_over']['born_before'](year)
			statistics['age_slices']['65_over']['gender'][gender]['count'] = (
				StatisticsBirthView.get_number_of_births_by_gender(max_inscription_date, gender,
					born_before=born_before)
					)

			for age_slice in statistics['age_slices'].values():
				statistics['num_readers'][gender] += age_slice['gender'][gender]['count']

				statistics['num_readers']['total'] = statistics['num_readers']['f'] + statistics['num_readers']['m']

				# Statistics by residence
				born_after = statistics['age_slices']['0_14']['born_after'](year)
				statistics['age_slices']['0_14']['resident']['count'] = (
				    StatisticsBirthView.get_number_of_birth_by_district(max_inscription_date, birth_arrondissement, born_after)
					)
				born_after = statistics['age_slices']['15_24']['born_after'](year)
				born_before = statistics['age_slices']['15_24']['born_before'](year)
				statistics['age_slices']['15_24']['resident']['count'] = (
					StatisticsBirthView.get_number_of_birth_by_district(max_inscription_date,
					birth_arrondissement, born_after, born_before)
						)
				born_after = statistics['age_slices']['25_64']['born_after'](year)
				born_before = statistics['age_slices']['25_64']['born_before'](year)
				statistics['age_slices']['25_64']['resident']['count'] = (
					StatisticsBirthView.get_number_of_birth_by_district(max_inscription_date,
					birth_arrondissement, born_after, born_before)
						)
				born_before = statistics['age_slices']['65_over']['born_before'](year)
				statistics['age_slices']['65_over']['resident']['count'] = (
					StatisticsBirthView.get_number_of_birth_by_district(max_inscription_date,
						birth_arrondissement, born_before=born_before)
					)

		def get_stats(self, year):
			from_date = date(year, 1, 1)
			to_date = date(year, 12, 31)
			statistics = {
				'num_readers': {'total': 0, 'f': 0, 'm': 0, 'resident': 0, 'non_resident': 0},
				'num_active_readers': (
					Birth.objects.filter(created_on__gte=from_date, created_on__lte=to_date)
					.values('nip').distinct().count()
				),
				'num_new_readers':  (
					BirthDeclaration.objects.filter(created_on__gte=from_date, created_on__lte=to_date).count()
						),
				'age_slices': self.age_slices
			}
			num_readers = Birth.eligible.count()
			# Age slices
			self.calculate_age_slices_stats(statistics, year)
			for slice_content in statistics['age_slices'].values():
				slice_content['count'] = slice_content['gender']['m']['count'] + slice_content['gender']['f']['count']
				slice_content['percent'] = round(slice_content['count'] / num_readers * 100, 2)
				slice_content['non_resident']['count'] = slice_content['count'] - slice_content['resident']['count']
				statistics['num_readers']['resident'] += slice_content['resident']['count']
				statistics['num_readers']['non_resident'] += slice_content['non_resident']['count']

			return statistics
