from django.urls import path

from camp_otter.core.views import PlaceDetailView, geocode_place_view

urlpatterns = [
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('place/<int:place_id>/geocode', geocode_place_view, name='geocode-place'),
]
