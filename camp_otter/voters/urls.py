from django.urls import path
from django.http import HttpResponse

from .views import VoterListView, FileUploadView, success, upload_file

urlpatterns = [
    path('', VoterListView.as_view(), name='voter-list'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('upload/success/', success, name='success')
]
