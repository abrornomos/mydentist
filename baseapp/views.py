from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _, get_language
from dentist.models import *
from .forms import *
from .models import *

# Create your views here.


def index(request):
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        geoform = GeoForm(request.POST)
        if searchform.is_valid() and geoform.is_valid():
            query = {
                'region': searchform.cleaned_data['region'],
                'gender': searchform.cleaned_data['gender'],
                'time': searchform.cleaned_data['time'],
                'nearest': searchform.cleaned_data['nearest'],
                'lat': geoform.cleaned_data['latitude'],
                'long': geoform.cleaned_data['longitude'],
            }
            request.session['query'] = query
            request.session['post'] = request.POST
        for key in request.session.keys():
            print(f"{key} - {request.session[key]}")
        return redirect("baseapp:results")
    else:
        geoform = GeoForm()
        if 'post' in request.session:
            searchform = SearchForm(request.session['post'])
            if searchform.is_valid():
                return render(request, "baseapp/index.html", {
                    'searchform': searchform,
                    'geoform': geoform
                })
            else:
                if 'query' in request.session:
                    return render(request, "baseapp/index.html", {
                        'searchform': searchform,
                        'geoform': geoform
                    })
        else:
            searchform = SearchForm()
            return render(request, "baseapp/index.html", {
                'searchform': searchform,
                'geoform': geoform
            })


def results(request):
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        geoform = GeoForm(request.POST)
        if searchform.is_valid() and geoform.is_valid():
            query = {
                'region': searchform.cleaned_data['region'],
                'gender': searchform.cleaned_data['gender'],
                'time': searchform.cleaned_data['time'],
                'nearest': searchform.cleaned_data['nearest'],
                'lat': geoform.cleaned_data['latitude'],
                'long': geoform.cleaned_data['longitude'],
            }
            request.session['query'] = query
            current_language = get_language()
            dentists_obj = Dentist.objects.filter(gender__pk=query['gender']).filter(is_fullday=query['time']).filter(clinic__region__pk=query['region']).filter(clinic__language__name=current_language)
            dentists = []
            for dentist in dentists_obj:
                clinic = Clinic.objects.get(pk=dentist.clinic_id)
                dentists.append({
                    'dentist': dentist,
                    'clinic': clinic
                })
            return render(request, "baseapp/results.html", {
                'searchform': searchform,
                'geoform': geoform,
                "dentists": dentists
            })
        else:
            return render(request, "baseapp/results.html", {
                'searchform': searchform,
                'geoform': geoform,
                "dentists": []
            })
    else:
        if 'query' in request.session:
            query = request.session['query']
            if 'post' in request.session:
                current_language = get_language()
                dentists_obj = Dentist.objects.filter(gender__pk=query['gender']).filter(is_fullday=query['time']).filter(clinic__region__pk=query['region']).filter(clinic__language__name=current_language)
                dentists = []
                for dentist in dentists_obj:
                    clinic = Clinic.objects.get(pk=dentist.clinic_id)
                    dentists.append({
                        'dentist': dentist,
                        'clinic': clinic
                    })
                searchform = SearchForm(request.session['post'])
                geoform = GeoForm()
                return render(request, "baseapp/results.html", {
                    'searchform': searchform,
                    'geoform': geoform,
                    "dentists": dentists
                })
            else:
                searchform = SearchForm({
                    'region': query['region'],
                    'gender': query['gender'],
                    'time': query['time'],
                    'nearest': query['nearest'],
                })
                geoform = GeoForm()
                return render(request, "baseapp/results.html", {
                    'searchform': searchform,
                    'geoform': geoform,
                    'dentists': []
                })
        else:
            searchform = SearchForm()
            geoform = GeoForm()
            return render(request, "baseapp/results.html", {
                'searchform': searchform,
                'geoform': geoform,
                'dentists': []
            })
