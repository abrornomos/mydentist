from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _, get_language
from dentist.models import *
from .forms import *
from .models import *
from .var import *
from .handler import *

# Create your views here.


def index(request):
    if request.method == "POST":
        request.session['post'] = request.POST
        return redirect("baseapp:results")
    else:
        searchform = SearchForm()
        geoform = GeoForm()
        authenticated = request.user.username in request.session
        language = get_language()
        language = Language.objects.get(name=language)
        services_obj = Service.objects.filter(
            dentist__clinic__language__pk=language.id
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
    authenticated = request.user.username in request.session
    if 'post' in request.session:
        searchform = SearchForm(request.session['post'])
        geoform = GeoForm(request.session['post'])
        if searchform.is_valid() and geoform.is_valid():
            services_obj = Service.objects.filter(
                name=searchform.cleaned_data['service']
            ).filter(
                dentist__clinic__region__pk=searchform.cleaned_data['region']
            )
            results_by_price = get_results(
                list(services_obj.order_by('price'))
            )
            results_by_distance = get_results(
                sort_by_distance(
                    list(services_obj),
                    (
                        geoform.cleaned_data['latitude'],
                        geoform.cleaned_data['longitude']
                    )
                )
            )
            return render(request, "baseapp/results.html", {
                "results": True,
                "results_by_price": results_by_price,
                "results_by_distance": results_by_distance,
                'authenticated': authenticated
            })
        else:
            return render(request, "baseapp/results.html", {
                'results': False,
                'authenticated': authenticated
            })
    else:
        return render(request, "baseapp/results.html", {
            'results': False,
            'authenticated': authenticated
        })
