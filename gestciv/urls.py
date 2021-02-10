from django.contrib import admin
from django.conf.urls import include, url
from gestciv import ajax
from gestciv import views 
import pdfkit

appName="gestciv"
urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'birth/save_father_form_to_session/(?P<dest_url>\S+)/$', views.save_father_form_to_session, name='save_father_form_to_session'),
    url(r'birth/save_mother_form_to_session/(?P<dest_url>\S+)/$', views.save_mother_form_to_session, name='save_mother_form_to_session'),
    url(r'birth/search_for_new_birth/(?P<dest_url>\S+)/$', views.search_for_new_birth, name='search_for_new_birth'),


#########################################################"
#
# Partie configuration
#
##########################################################
    url(r'departement/add/$', views.DepCreateView.as_view(), name='dept_add'),



#########################################################


    url(r'birthdeclare/search_for_new_birth/(?P<dest_url>\S+)/$', views.search_for_new_birth, name='search_for_new_birth'),
    url(r'birthdeclare/nbadd/$', views.BirthDeclarationCreateView.as_view(), name='nbirth_add'),
    url(r'birthdeclare/nbadd/(?P<nip>\w+)$', views.BirthDeclarationCreateView.as_view(), name='nbirth_add'),
    url(r'birthdeclare/list/$', views.BirthDeclarationListView.as_view(), name='nbirth_list'),
    url(r'birthdeclare/list/(?P<display>\w+)/$', views.BirthDeclarationListView.as_view(), name='nbirth_list'),
    url(r'birthdeclararation/(?P<pk>\d+)/$', views.BirthDeclarationUpdateView.as_view(), name='nbirth_update'),

    url(r'birth/add/(?P<from_external_page>\w+)?$', views.BirthCreateView.as_view(), name='birth_add'),
    url(r'birth/(?P<pk>\d+)/delete/$', views.BirthDeleteView.as_view(), name='birth_delete'),
    url(r'birth/add/(?P<pk>\d+)/$', views.BirthFormUniqueNumber, name='birth_add'),
    url(r'birth/certificate/import/$', views.BirthDeclarationImportView.as_view(), name='birth_declaration_import'),
    url(r'birth/genpdf/(?P<birth_id>\d+)$', views.gen_acte_naissance, name='gen_ec_pdf'),
#    url(r'birth/genpdf/(?P<birth_id>\d+)$', views.gen_possession_etat_pdf, name='gen_pe_pdf'),
    url(r'birth/list/$', views.BirthListView.as_view(), name='birth_list'),
    url(r'birth/list/(?P<nip>\w+)/$', views.BirthListView.as_view(), name='birth_list'),
    url(r'birth/list/(?P<nip>\w+)/$', views.BirthListView.as_view(), name='birth_list'),
    url(r'birth/(?P<pk>\d+)/$', views.BirthUpdateView.as_view(), name='birth_update'),


    url(r'death/declaration/$', views.DeathDeclarationView.as_view(), name='death_declaration'),
#    url(r'birth/genpdf/(?P<birth_id>\d+)$', views.gen_acte_naissance, name='gen_ec_pdf'),
#    url(r'birth/genpdf/(?P<birth_id>\d+)$', views.gen_possession_etat_pdf, name='gen_pe_pdf'),
#    url(r'birth/list/$', views.BirthListView.as_view(), name='birth_list'),
#    url(r'birth/list/(?P<nip>\w+)/$', views.BirthListView.as_view(), name='birth_list'),
#    url(r'birth/list/(?P<nip>\w+)/$', views.BirthListView.as_view(), name='birth_list'),
#    url(r'birth/(?P<pk>\d+)/$', views.BirthUpdateView.as_view(), name='birth_update'),


    url(r'registration/add/(?P<redirect_to_birth>\w+)?$', views.RegistrationCreateView.as_view(), name='registration_add'),
    url(r'registration/update/(?P<pk>\d+)/$', views.RegistrationUpdateView.as_view(), name='registration_update'),
#    url(r'registration/update/(?P<pk>\d+)/$', views.RegistrationUpdateView.as_view(), name='registration_update'),
    url(r'registration/delete/(?P<pk>\d+)/delete/$', views.RegistrationDeleteView.as_view(), name='registration_delete'),
    url(r'registration/list/$', views.RegistrationListView.as_view(), name='registration_list'),
    url(r'registration/genpepdf/(?P<registration_id>\d+)$', views.gen_possession_etat_pdf, name='gen_pe_pdf'),
    url(r'registration/genarpdf/(?P<registration_id>\d+)$', views.gen_attestation_residence_pdf, name='gen_ar_pdf'),
    url(r'ajax/get/get_mairie_arrondissement/?$', ajax.get_mairie_arrondissement, name='get_mairie_arrondissement'),
    url(r'ajax/get/get_default_arrondissement/?$', ajax.get_default_arrondissement, name='get_default_arrondissement'),
    url(r'ajax/get/get_arrondissement_quartier/?$', ajax.get_arrondissement_quartier, name='get_arrondissement_quartier'),
    url(r'ajax/get/get_default_arrondissement/?$', ajax.get_default_arrondissement, name='get_default_arrondissement'),
    url(r'statistics/registration/$', views.StatisticsRegistrationView.as_view(), name='statistics_registration'),
    url(r'statistics/birth/$', views.StatisticsBirthView.as_view(), name='statistics_birth'),

    url(r'death/add/$', views.DeathCreateView.as_view(), name='death_add'),
]

