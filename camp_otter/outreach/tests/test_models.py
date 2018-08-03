from django.test import TestCase

from camp_otter.core.models import Place
from camp_otter.voters.models import Voter
from camp_otter.outreach.models import OutreachList

import pandas as pd

class OutreachListModelTests(TestCase):

    def test_empty_outreach_list_object_create(self):
        mylist = OutreachList(name='My Test List')
        mylist.save()
        self.assertEqual(OutreachList.objects.get(name='My Test List').name, 'My Test List')

    def test_add_voter_to_list(self):
        mylist = OutreachList(name='My Test List')
        mylist.save()
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', date_of_birth='1988-01-23',
                                               residence=house, voter_id=112341)
        voter.save()
        self.assertEqual(mylist.outreachcontact_set.count(), 0)
        OutreachList.objects.add_voter_to_list(mylist, voter.person)
        self.assertEqual(mylist.outreachcontact_set.count(), 1)

    def test_dataframe_output(self):
        mylist = OutreachList(name='My Test List')
        mylist.save()
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI')
        house.save()
        voter = Voter.objects.create_new_voter(first_name='Joe', last_name='Test', date_of_birth='1988-01-23',
                                               residence=house, voter_id=112341)
        voter.save()
        voter2 = Voter.objects.create_new_voter(first_name='Steve', last_name='Voter', date_of_birth='1960-2-22',
                                                residence=house, voter_id=5312)
        voter2.save()
        OutreachList.objects.add_voter_to_list(mylist, voter.person)
        OutreachList.objects.add_voter_to_list(mylist, voter2.person)
        print(mylist.as_blank_dataframe())
