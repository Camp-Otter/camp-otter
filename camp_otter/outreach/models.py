from django.db import models
from django.urls import reverse

from camp_otter.core.models import Campaign, CampaignStaff, GroupObject, GroupRelation, Person
from camp_otter.voters.models import Voter


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
