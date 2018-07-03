from django.test import TestCase
from camp_otter.voters.models import Voter, VoterGroup
from camp_otter.core.models import Place, Person, Election, GroupRelation, GroupObject


class VoterModelTests(TestCase):

    def test_create_new_voter(self):
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', date_of_birth='1988-01-23',
                                               residence=house, voter_id=112341)
        self.assertEqual(str(voter), 'Test, Joe')

    def test_create_voter_from_person(self):
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='2000-12-12', residence=house)
        person.save()
        voter = Voter.objects.create_voter_from_person(person=person, voter_id=12304)
        self.assertEqual(str(voter), 'Test, Joe')

    def test_add_election(self):
        election = Election(election_date='2016-11-08')
        election.save()
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', date_of_birth='1988-01-23',
                                               residence=house, voter_id=112341)
        voter.save()
        voter.add_election(election=election, precinct=1000)
        #self.assert(election.voterparticipation_set.all(), voter.voterparticipation_set.all())


class VoterGroupTests(TestCase):

    def test_voter_group_inheritance(self):
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', date_of_birth='1988-01-23',
                                               residence=house, voter_id=112341)
        myvoters = VoterGroup(name='Blue', party='DEM')
        myvoters.save()
        myrel = GroupRelation(group=myvoters, content_object=voter)
        myrel.save()
        self.assertEqual(myrel.group.party, 'DEM')