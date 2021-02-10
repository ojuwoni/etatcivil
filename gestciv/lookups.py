# -*- coding: utf-8 -*-
"""
Ajax autocomplete stuff
"""

from django.db.models import Q

from ajax_select import LookupChannel, register
from gestciv.models import Registration,BirthDeclaration


@register('father_list')
class FatherLookup(LookupChannel):
	model = Registration

	def get_query(self, q, request):
		return Registration.objects.all().filter(sex__iexact='M').filter((Q(
				firstname__icontains=q.upper()) | Q(lastname__icontains=q.title()))
				).order_by('lastname')

@register('mother_list')
class MotherLookup(LookupChannel):
	model = Registration

	def get_query(self, q, request):
		return Registration.objects.all().filter(sex__iexact='F').filter((Q(
				firstname__icontains=q.upper()) | Q(lastname__icontains=q.title()))
					).order_by('lastname')

#		return Registration.objects.filter(
#			(Q(firstname__icontains=q.upper()) | Q(lastname__icontains=q.title()))
#					).order_by('lastname')
	

@register('declarant_list')
class DeclarantLookup(LookupChannel):
    model = Registration

    def get_query(self, q, request):
        return Registration.objects.filter(
            Q(firstname__icontains=q.upper()) | Q(lastname__icontains=q.title())
        ).order_by('lastname')

@register('nip_list')
class NipLookup(LookupChannel):
    model = BirthDeclaration

    def get_query(self, q, request):
        return BirthDeclaration.objects.search(nip__icontains=q.title).order_by('nip')


