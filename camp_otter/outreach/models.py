from django.db import models

from camp_otter.core.models import Campaign, CampaignStaff
from camp_otter.voters.models import Voter


class OutreachList(models.Model):
    list_name = models.CharField(max_length=250)
    voters = models.ManyToManyField(Voter, blank=True)  # allow an empty list so it can be built in a manual workflow

    # https://stackoverflow.com/questions/4959499/how-to-add-multiple-objects-to-manytomany-relationship-at-once-in-django/32266913
