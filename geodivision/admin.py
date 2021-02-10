from django.contrib import admin
from geodivision.models import (Profession, Departement, Mairie,  Arrondissement, Quartier) 


class ProfessionAdmin(admin.ModelAdmin):
	list_display = ('code','nom')
	search_fields=('code', 'nom')
admin.site.register(Profession, ProfessionAdmin)

class DepartementAdmin(admin.ModelAdmin):
    list_display = ('c_dep','nom')
    search_fields = ('c_dep','nom')
admin.site.register(Departement, DepartementAdmin)

class MairieAdmin(admin.ModelAdmin):
    list_display = ('c_com','departement','nom','adresse','is_default')
    search_fields = ('code','nom','departement')
admin.site.register(Mairie, MairieAdmin)

class ArrondissementAdmin(admin.ModelAdmin):
    list_display = ('c_arr','mairie','nom','adresse')
    search_fields = ('c_arr','mairie')
admin.site.register(Arrondissement, ArrondissementAdmin)

class QuartierAdmin(admin.ModelAdmin):
    list_display = ('c_qua','arrondissement','nom','adresse')
    search_fields = ('c_qua','arrondissement')
admin.site.register(Quartier, QuartierAdmin)



