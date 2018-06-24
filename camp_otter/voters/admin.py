from django.contrib import admin
from camp_otter.voters.models import Voter, VoterParticipation

# Register your models here.
admin.site.register(Voter)
admin.site.register(VoterParticipation)