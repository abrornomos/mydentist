from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _, get_language
from json import dumps
from dentist.models import User as DentistUser, Service_translation
from patient.models import User as PatientUser
from mydentist.handler import *
from mydentist.var import REGIONS
from .forms import *
from .models import *


def index(request):
    if request.method == "POST":
        request.session['post'] = request.POST
        return redirect("baseapp:results")
    else:
        try:
            del request.session['post']
        except:
            pass
        searchform = SearchForm()
        geoform = GeoForm()
        authenticated = is_authenticated(request, "patient") or is_authenticated(request, "dentist")
        if authenticated:
            try:
                user = PatientUser.objects.get(user__username=request.user.username)
                authenticated = "patient"
                check_language(request, "patient")
            except:
                try:
                    user = DentistUser.objects.get(user__username=request.user.username)
                    authenticated = "dentist"
                except:
                    pass
        language = Language.objects.get(name=get_language())
        services_obj = Service_translation.objects.filter(
            language__pk=language.id
        ).values('name').annotate(
            name_count=Count('name')
        )
        services = []
        for i in range(len(services_obj)):
            services.append({
                'value': services_obj[i]['name'],
                'name': services_obj[i]['name']
            })
        return render(request, "baseapp/index.html", {
            'searchform': searchform,
            'regions': REGIONS,
            'region': REGIONS[0],
            'services': services,
            'service': services[0],
            'geoform': geoform,
            'authenticated': authenticated
        })


def results(request):
    authenticated = is_authenticated(request, "patient") or is_authenticated(request, "dentist")
    if authenticated:
        try:
            user = PatientUser.objects.get(
                user__username=request.user.username)
            authenticated = "patient"
            check_language(request, "patient")
        except:
            try:
                user = DentistUser.objects.get(
                    user__username=request.user.username)
                authenticated = "dentist"
            except:
                pass
    return render(request, "baseapp/results.html", {
        'authenticated': authenticated
    })


def get_dentists(request):
    if 'post' in request.session:
        searchform = SearchForm(request.session['post'])
        geoform = GeoForm(request.session['post'])
        if searchform.is_valid() and geoform.is_valid():
            if request.POST['sort_by'] == "price":
                services_obj = Service_translation.objects.filter(
                    name=searchform.cleaned_data['service'],
                    service__dentist__clinic__region__pk=searchform.cleaned_data['region']
                )
                if request.POST['female'] == "true" and request.POST['time'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True
                    )
                elif request.POST['female'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__gender__pk=2
                    )
                elif request.POST['time'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__is_fullday=True
                    )
                results = get_results(
                    list(services_obj.order_by('service__price'))
                )
            elif request.POST['sort_by'] == "near":
                services_obj = Service_translation.objects.filter(
                    name=searchform.cleaned_data['service'],
                    service__dentist__clinic__region__pk=searchform.cleaned_data['region']
                )
                if request.POST['female'] == "true" and request.POST['time'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True
                    )
                elif request.POST['female'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__gender__pk=2
                    )
                elif request.POST['time'] == "true":
                    services_obj = Service_translation.objects.filter(
                        name=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__is_fullday=True
                    )
                results = get_results(
                    sort_by_distance(
                        list(services_obj),
                        (
                            geoform.cleaned_data['latitude'],
                            geoform.cleaned_data['longitude']
                        )
                    )
                )
            response = HttpResponse(dumps(results))
            return response
        else:
            response = HttpResponse()
            response.status_code = 404
            return response
    else:
        response = HttpResponse()
        response.status_code = 404
        return response
