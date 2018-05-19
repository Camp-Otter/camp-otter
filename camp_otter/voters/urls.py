from django.urls import path

from camp_otter.voters.views import VoterListView

urlpatterns = [
    path('', VoterListView.as_view(), name='voter-list')
]