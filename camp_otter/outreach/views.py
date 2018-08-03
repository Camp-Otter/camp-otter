from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from camp_otter.outreach.models import Survey, SurveyQuestion


class OutreachHome(View):

    pass


class SurveyCreate(CreateView):
    model = Survey
    fields = ['survey_name', 'questions']


class SurveyDetail(DetailView):
    model = Survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


class SurveyQuestionCreate(CreateView):
    model = SurveyQuestion
    fields = ['question_text']


class SurveyQuestionDetail(DetailView):
    model = SurveyQuestion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context