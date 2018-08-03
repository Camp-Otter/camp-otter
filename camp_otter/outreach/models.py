from django.db import models
from django.urls import reverse

from camp_otter.core.models import Campaign, CampaignStaff, GroupObject, GroupRelation, Person
from camp_otter.voters.models import Voter

import pandas as pd
import numpy as np


class OutreachListManager(models.Manager):
    # TODO: confirm that a manager is needed here

    def add_voter_to_list(self, list_object, person):
        contact = OutreachContact(person=person, contact_list=list_object)
        contact.save()

    def create_list_from_group(self, group, list_name=None):
        # create new list object
        if list_name is None:
            list_name = group.name
        new_list = OutreachList(name=list_name)

        # copy all GroupRelations and link to new list
        rel_set = group.grouprelation_set.objects.all()
        # copy over to
        new_list.save()

    def create_walklist(self):
        pass

    def export_list_to_excel(self, list_object):
        # stub for formatting and exporting to excel
        pass


class SurveyQuestion(models.Model):
    question_text = models.CharField(max_length=300)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})


class Survey(models.Model):
    survey_name = models.CharField(max_length=250)
    questions = models.ManyToManyField(SurveyQuestion)

    def __str__(self):
        return self.survey_name

    def get_absolute_url(self):
        return reverse('survey-detail', kwargs={'pk': self.pk})


class OutreachList(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True)
    list_completed = models.BooleanField(default=False)
    list_completed_on = models.DateField(null=True)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, null=True)
    group = models.ForeignKey(GroupObject, on_delete=models.PROTECT, null=True)

    objects = OutreachListManager()

    # TODO: get all residences of people in OutreachList

    def as_blank_dataframe(self):
        """
        Generate a template dataframe or the outreach list to populate data
        :return:
        """
        contact_items = self.outreachcontact_set.all()
        person_list = [c.person for c in contact_items]
        # TODO: sort out phone lists for multiple phone numbers
        # questions = pd.Series([s.question for s in [c.surveyresponse_set.all() for c in contact_items]]]).drop_duplicates().tolist()

        questions = []

        for c in contact_items:
            survey_responses = list(c.surveyresponse_set.all())
            q = [s.question for s in survey_responses]
            questions.extend(q)

        questions = pd.Series(questions).drop_duplicates().tolist()

        # TODO: this is for a walk list only.  make generic for any contact type.
        person_df_columns = ['first_name', 'last_name', 'street_number', 'street_name', 'street_name_2', 'unit', 'street_suffix']
        person_first_names = [p.first_name for p in person_list]
        person_last_names = [p.last_name for p in person_list]
        # person_suffix = [p.suffix for p in person_list]
        person_street_number = [p.residence.street_number for p in person_list]
        person_street_name = [p.residence.street_name for p in person_list]
        person_street_name_2 = [p.residence.street_name_2 for p in person_list]
        person_unit = [p.residence.unit for p in person_list]
        person_street_suffix = [p.residence.suffix_a for p in person_list]

        person_list = list(zip(person_first_names, person_last_names, person_street_number,
                           person_street_name, person_street_name_2, person_unit, person_street_suffix))
        df = pd.DataFrame(person_list, columns=person_df_columns)
        df[questions] = np.nan
        return df



class OutreachContactManager(models.Manager):
    pass


class OutreachContact(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, null=True)
    contacted_by = models.ForeignKey(CampaignStaff, on_delete=models.PROTECT, null=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    contact_list = models.ForeignKey(OutreachList, on_delete=models.PROTECT, null=True)
    contacted = models.BooleanField(default=False)
    contacted_on = models.DateTimeField(null=True)
    METHOD_CHOICES = (
        ('Phone', 'PH'),
        ('Email', 'EM'),
        ('Door', 'DOOR')
    )
    contact_method = models.CharField(max_length=4, choices=METHOD_CHOICES)
    notes = models.TextField(blank=True)


class SurveyResponse(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT)
    response_text = models.CharField(max_length=250)
    outreach_contact_event = models.ForeignKey(OutreachContact, on_delete=models.PROTECT)
