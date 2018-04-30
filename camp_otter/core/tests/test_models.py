from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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

    def test_return_multiple_residents(self):
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        house.save()
        person1 = Person(first_name='Steve', last_name='Test', residence=house)
        person1.save()
        person2 = Person(first_name='Joe', last_name='Test', residence=house)
        person2.save()
        self.assertQuerysetEqual(house.person_set.all(), [repr(person1), repr(person2)], ordered=False)

    def test_spatial_field(self):
        house = Place(street_address='1 Broadway', city='Newport', state='RI')
        house.save()
        house.geocode()
        self.assertEqual(str(house.point.y), '41.490611')


class PersonModelTests(TestCase):

    def test_person_string_method(self):
        person = Person(first_name='Steve', last_name='Test')
        self.assertEquals(str(person), 'Test, Steve')


class ContactPhoneModelTests(TestCase):

    def test_create_phone_number(self):
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', residence=house)
        person.save()
        number = '5552345'
        phone = ContactPhone(phone_number=number, person=person)
        phone.save()
        self.assertEqual(ContactPhone.objects.filter(phone_number=number).count(), 1)
        self.assertQuerysetEqual(person.contactphone_set.all(), [repr(phone)], ordered=False)


class ContactEmailModelTests(TestCase):

    def test_create_email(self):
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', residence=house)
        person.save()
        email_addr = 'joe@example.com'
        email = ContactEmail(email=email_addr, person=person)
        email.save()
        self.assertEqual(ContactEmail.objects.filter(email=email_addr).count(), 1)
        self.assertQuerysetEqual(person.contactemail_set.all(), [repr(email)], ordered=False)


class ElectionModelTests(TestCase):

    # TODO: build Election model tests

    pass


class BallotQuestionModelTests(TestCase):

    def test_ballotquestion_string_method(self):
        question = BallotQuestion(question_text='Test question')
        self.assertEquals(str(question), 'Test question')

    def test_add_choices_to_ballot(self):
        election = Election(election_date='2018-01-01')
        election.save()
        question = BallotQuestion(question_text='Should we do that?', election=election)
        question.save()
        camp1 = Campaign(campaign_name='Yes', ballot_question=question)
        camp1.save()
        camp2 = Campaign(campaign_name='No', ballot_question=question)
        camp2.save()

        # https://docs.djangoproject.com/en/2.0/topics/testing/tools/#django.test.TransactionTestCase.assertQuerysetEqual
        self.assertQuerysetEqual(question.campaign_set.all(), [repr(camp1), repr(camp2)], ordered=False)


class CampaignModelTests(TestCase):

    def test_campaign_string_method(self):
        campaign = Campaign(campaign_name='Yes')
        self.assertEquals(str(campaign), 'Yes')

    def test_get_campaign_staff_list(self):
        election = Election(election_date='2018-01-01')
        election.save()
        question = BallotQuestion(question_text='Should we do that?', election=election)
        question.save()
        camp1 = Campaign(campaign_name='Yes', ballot_question=question)
        camp1.save()
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        house.save()
        person1 = Person(first_name='Steve', last_name='Test', residence=house)
        person1.save()
        person2 = Person(first_name='Joe', last_name='Test', residence=house)
        person2.save()
        staff1 = CampaignStaff(staff_memeber=person1, campaign_name=camp1, position='Volunteer')
        staff2 = CampaignStaff(staff_memeber=person2, campaign_name=camp1, position='Manager')
        staff1.save()
        staff2.save()
        self.assertQuerysetEqual(camp1.campaignstaff_set.all(),[repr(staff1), repr(staff2)], ordered=False)


class CampaignStaffModelTests(TestCase):

    def test_staff_string_method(self):
        house = Place(street_address='1 Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', residence=house)
        person.save()
        election = Election(election_date='2018-01-01')
        election.save()
        question = BallotQuestion(question_text='Should we do that?', election=election)
        question.save()
        camp1 = Campaign(campaign_name='Yes', ballot_question=question)
        camp1.save()
        staffer = CampaignStaff(staff_memeber=person, campaign_name=camp1, position='Tester')
        self.assertEqual(str(staffer), str(person))
