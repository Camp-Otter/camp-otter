from django.urls import path
from django.http import HttpResponse

from .views import OutreachHome, SurveyCreate, SurveyDetail, SurveyQuestionCreate, SurveyQuestionDetail

urlpatterns = [
    path('', OutreachHome.as_view(), name='outreach-home'),
    path('survey/create', SurveyCreate.as_view(), name='create-survey'),
    path('survey/<int:pk>', SurveyDetail.as_view(), name='survey-detail'),
    path('survey/question/create', SurveyQuestionCreate.as_view(), name='create-question'),
    path('survey/question/<int:pk>/', SurveyQuestionDetail.as_view(), name='question-detail'),
]
