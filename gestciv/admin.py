from django.contrib import admin
from gestciv.models import (Registration, Birth, AppliNews,  GeneralConfiguration, Maternite, 
				BirthDeclaration, UserProfile, Profession)


class ProfessionAdmin(admin.ModelAdmin):
	list_display = ('code','nom')
	search_fields=('code', 'nom')
admin.site.register(Profession, ProfessionAdmin)

class MaterniteAdmin(admin.ModelAdmin):
        list_display = ('c_mat','nom')
        search_fields=('c_mat', 'nom')
admin.site.register(Maternite, MaterniteAdmin)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo', 'profession', 'phone', 'organization')
	search_fields = ('user', 'profession')
admin.site.register(UserProfile, UserProfileAdmin)

class RegistrationAdmin(admin.ModelAdmin):
        list_display = ('nip','title', 'lastname', 'young_girl_lastname', 'firstname', 'sex', 'status', 
				'birthday', 'nationality', 'job','city', 'district', 'street_type', 
				'phone', 'mail','created_by', 'created')

        list_filter = ('firstname','birthday')
        search_fields = ('firstname','birthday')
#        prepopulated_fields = {'slug': ('title',)}
#        raw_id_fields = ('lastname',)
        date_hierarchy = 'created'
        ordering = ['firstname', 'sex']
admin.site.register(Registration, RegistrationAdmin)

class BirthDeclarationAdmin(admin.ModelAdmin):
	list_display = ('id','nip','sex','birthweight','birthday','birthhour','neighborhood',
			'mother', 'midwife', 'district', 'mairie','bcduedate', 'can_be_issued')
	list_filter = ('nip', 'mother')
	search_fields = ('nip', 'mother')

admin.site.register(BirthDeclaration, BirthDeclarationAdmin)

class BirthAdmin(admin.ModelAdmin):
	list_display = ('id','nip','firstname','sex','birthweight','birthday','birthhour',
			'district','social_number')
	list_filter = ('firstname', 'birthday')
	search_fields = ('firstname', 'birthday')

admin.site.register(Birth, BirthAdmin)

class AppliNewsAdmin(admin.ModelAdmin):
	list_display = ('publish_date', 'news')

admin.site.register(AppliNews, AppliNewsAdmin)
admin.site.register(GeneralConfiguration)
