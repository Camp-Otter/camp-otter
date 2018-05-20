from django.db import models
from camp_otter.core.models import Person, Election

# Create your models here.
class VoterManager(models.Manager):

    def create_new_voter(self, first_name, last_name, residence, voter_id):
        person=Person(first_name=first_name, last_name=last_name, residence=residence)
        person.save()
        voter = self.create(person=person, voter_id=voter_id)
        return voter

    def create_voter_from_person(self, person, voter_id):
        """
        Create a voter from an existing Person object
        :param Person:
        :return:
        """
        voter = self.create(person=person, voter_id=voter_id)
        return voter


class Voter(models.Model):
    person = models.OneToOneField(Person, on_delete=models.PROTECT)
    voter_id = models.BigIntegerField()

    # use an object manager to handle object creation
    objects = VoterManager()

    def __str__(self):
        return str(self.person)

    def add_election(self, election, precinct):
        election = VoterParticipation(voter=self, election=election, precinct=precinct)
        election.save()


class VoterParticipation(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.PROTECT)
    election = models.ForeignKey(Election, on_delete=models.PROTECT)
    precinct = models.IntegerField()
