from django.urls import path

from camp_otter.core.views import PlaceDetailView, geocode_place_view, BasicMapView, GeoJsonAPI

urlpatterns = [
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('place/<int:place_id>/geocode', geocode_place_view, name='geocode-place'),
    path('place/data/geojson', GeoJsonAPI.as_view(), name='places-data'),
    # TODO: add parameters to make this a better API call
    path('map', BasicMapView.as_view(), name='places-map'),
]
