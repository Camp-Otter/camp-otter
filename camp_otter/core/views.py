from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, TemplateView, View
from django.core.serializers import serialize

from .models import Place


# Create your views here.
class PlaceDetailView(DetailView):

    model = Place

class BasicMapView(TemplateView):

    template_name = "core/map.html"


class GeoJsonAPI(View):
    # a view to manage place geojson data.  GET requests return all places serialized as geojson.

    def get(self, request):
        # TODO: more parameters could be passed to provide other filters
        geojson_out = serialize('geojson', Place.objects.all(), geometry_field='point')
        return HttpResponse(geojson_out, content_type='application/json')


def geocode_place_view(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place.geocode()
    return redirect(reverse('place-detail', args=[place_id]))
