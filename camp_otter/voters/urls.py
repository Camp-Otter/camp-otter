from django.urls import path
from django.http import HttpResponse

from .views import VoterListView, VoterFileUploadView, HistoryFileUploadView, VoterDetailView, success

urlpatterns = [
    path('', VoterListView.as_view(), name='voter-list'),
    path('<int:pk>/', VoterDetailView.as_view(), name='voter-detail'),
    path('voter-upload/', VoterFileUploadView.as_view(), name='voter-upload'),
    path('history-upload/', HistoryFileUploadView.as_view(), name='history-upload'),
    path('upload/success/', success, name='success')
]
