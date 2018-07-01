from django.urls import path
from django.http import HttpResponse

from .views import OutreachHome

urlpatterns = [
    path('', OutreachHome.as_view(), name='outreach-home'),
]
