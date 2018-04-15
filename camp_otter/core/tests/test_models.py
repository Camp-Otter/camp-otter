from django.test import TestCase
from camp_otter.core.models import Place, Person, ContactPhone, ContactEmail, Election, BallotQuestion, Campaign, CampaignStaff

# Tests for core models


class PlaceModelTests(TestCase):

    def test_address_string_method(self):
        #  The __str__ method on a Place provides conditional logic on how to format the string.
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        self.assertEquals(str(house), '1 Main St., Newport, RI')
        landmark = Place(place_name='The Breakers', street_address='200 Bellevue Ave', city='Newport', state='RI')
        self.assertEquals(str(landmark), 'The Breakers')
        appartment = house
        appartment.unit = '22'
        self.assertEquals(str(appartment), '22 1 Main St., Newport, RI')


class PersonModelTests(TestCase):

    def test_person_string_method(self):
        person = Person(first_name='Steve', last_name='Test')
        self.assertEquals(str(person), 'Test, Steve')


class ContactPhoneModelTests(TestCase):

    # TODO: build ContactPhone model tests

    pass


class ContactEmailModelTests(TestCase):

    # TODO: build ContactEmail model tests

    pass


class ElectionModelTests(TestCase):

    # TODO: build Election model tests

    pass


class BallotQuestionModelTests(TestCase):

    def test_ballotquestion_string_method(self):
        question = BallotQuestion(question_text='Test question')
        self.assertEquals(str(question), 'Test question')


class CampaignModelTests(TestCase):

    # TODO: build Campaign model tests

    pass


class CampaignStaffModelTests(TestCase):

    # TODO: build CampaignStaff model tests

    pass
