# -*- coding: utf-8 -*-
"""
Various Ajax stuff
"""

import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gestciv.models import Mairie, Arrondissement, Quartier

@csrf_exempt
def get_default_arrondissement(request):
    response = {}
    data = []
    if request.POST['district_id']:
        arrondissements = Arrondissement.get_arrondissement()
        for arrondissement in arrondissements:
            data.append({'id': arrondissement.id, 'name': arrondissement.nom})
        response = {'item_list':data}
    return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def get_mairie_arrondissement(request):
    response = {}
    data = []
    if request.POST['city_id']:
        arrondissements = Arrondissement.objects.filter(mairie=int(request.POST['city_id']))
        for arrondissement in arrondissements:
            data.append({'id': arrondissement.id, 'name': arrondissement.nom})
        response = {'item_list':data}
    return HttpResponse(simplejson.dumps(response))


@csrf_exempt
def get_arrondissement_quartier(request):
    response = {}
    data = []
    if request.POST['district_id']:
        quartiers = Quartier.objects.filter(arrondissement=int(request.POST['district_id']))
        for quartier in quartiers:
            data.append({'id': quartier.id, 'name': quartier.nom})
        response = {'item_list':data}
    return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def get_default_arrondissement(request):
    response = {}
    data = []
    if request.POST['district_id']:
        arrondissements = Arrondissement.objects.filter(mairie=Mairie.get_default_mairie())
        for arrondissement in arrondissements:
            data.append({'id': arrondissement.id, 'name': arrondissement.nom})
        response = {'item_list':data}
    return HttpResponse(simplejson.dumps(response))
