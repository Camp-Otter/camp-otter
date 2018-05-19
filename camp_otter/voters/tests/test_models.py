from django.test import TestCase
from camp_otter.voters.models import Voter
from camp_otter.core.models import Place, Person, Election


class VoterModelTests(TestCase):

    def test_create_new_voter(self):
        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', residence=house, voter_id=112341)
        self.assertEqual(str(voter), 'Test, Joe')

    def test_create_voter_from_person(self):
        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', residence=house)
        person.save()
        voter = Voter.objects.create_voter_from_person(person=person, voter_id=12304)
        self.assertEqual(str(voter), 'Test, Joe')

    def test_add_election(self):
        election = Election(election_date='2016-11-08')
        election.save()
        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', residence=house, voter_id=112341)
        voter.save()
        voter.add_election(election=election, precinct=1000)
        #self.assert(election.voterparticipation_set.all(), voter.voterparticipation_set.all())
