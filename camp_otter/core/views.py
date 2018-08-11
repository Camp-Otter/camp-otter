from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView

from .models import Place


# Create your views here.
class PlaceDetailView(DetailView):

    model = Place


def geocode_place_view(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place.geocode()
    return redirect(reverse('place-detail', args=[place_id]))
