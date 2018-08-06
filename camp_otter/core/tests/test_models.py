from django.test import TestCase
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.gdal import DataSource
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from camp_otter.core.models import Place, Person, ContactPhone, \
    ContactEmail, Election, BallotQuestion, Campaign, CampaignStaff, MailingAddress, GroupObject, GroupRelation

import datetime
# Tests for core models


class PlaceModelTests(TestCase):

    def test_address_string_method(self):
        #  The __str__ method on a Place provides conditional logic on how to format the string.
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI', zip_code='02840')
        self.assertEquals(str(house), '1 Main St, Newport, RI 02840')
        landmark = Place(place_name='The Breakers', street_number='200', street_name='Bellevue Ave', city='Newport', state='RI')
        self.assertEquals(str(landmark), 'The Breakers')
        appartment = house
        appartment.unit = '22'
        self.assertEquals(str(appartment), '1 Main St, Unit 22, Newport, RI 02840')

    def test_return_multiple_residents(self):
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person1 = Person(first_name='Joe', last_name='Test', date_of_birth='1988-01-01', residence=house)
        person1.save()
        person2 = Person(first_name='Steve', last_name='Voter', date_of_birth='1982-11-21', residence=house)
        person2.save()
        self.assertQuerysetEqual(house.person_set.all(), [repr(person1), repr(person2)], ordered=False)

    def test_spatial_field(self):
        house = Place(street_number=1, street_name='Broadway', city='Newport', state='RI', zip_code='02840')
        house.save()
        self.assertEqual(str(house.point.y), '0.0')
        house.geocode()
        self.assertEqual(str(house.point.y), '41.4905123430452')


class MailingAddressModelTests(TestCase):

    def test_mailing_address_default_on_person_create(self):
        # TODO: a mailing address object should be created by the person object unless explicitly blocked
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1988-01-01', residence=house)
        person.save()
        self.assertEqual(MailingAddress.objects.count(), 1)
        self.assertQuerysetEqual(MailingAddress.objects.all(), Place.objects.all())


class PersonModelTests(TestCase):

    def test_person_string_method(self):
        person = Person(first_name='Steve', last_name='Test')
        self.assertEquals(str(person), 'Test, Steve')


class ContactPhoneModelTests(TestCase):

    def test_create_phone_number(self):
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1988-01-01', residence=house)
        person.save()
        number = '5552345'
        phone = ContactPhone(phone_number=number, person=person)
        phone.save()
        self.assertEqual(ContactPhone.objects.filter(phone_number=number).count(), 1)
        self.assertQuerysetEqual(person.contactphone_set.all(), [repr(phone)], ordered=False)


class ContactEmailModelTests(TestCase):

    def test_create_email(self):
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1988-01-01', residence=house)
        person.save()
        email_addr = 'joe@example.com'
        email = ContactEmail(email=email_addr, person=person)
        email.save()
        self.assertEqual(ContactEmail.objects.filter(email=email_addr).count(), 1)
        self.assertQuerysetEqual(person.contactemail_set.all(), [repr(email)], ordered=False)


class ElectionModelTests(TestCase):

    def test_election_with_date_object(self):
        election = Election(election_date=datetime.datetime.strptime('2016-11-08', "%Y-%m-%d").date(), election_type='GENERAL ELECTION')


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
        house = Place(street_number='1', street_name='Main St.', city='Newport', state='RI')
        house.save()
        person1 = Person(first_name='Steve', last_name='Test', date_of_birth='1986-02-22', residence=house)
        person1.save()
        person2 = Person(first_name='Joe', last_name='Test', date_of_birth='1990-12-12', residence=house)
        person2.save()
        staff1 = CampaignStaff(staff_memeber=person1, campaign_name=camp1, position='Volunteer')
        staff2 = CampaignStaff(staff_memeber=person2, campaign_name=camp1, position='Manager')
        staff1.save()
        staff2.save()
        self.assertQuerysetEqual(camp1.campaignstaff_set.all(),[repr(staff1), repr(staff2)], ordered=False)


class CampaignStaffModelTests(TestCase):

    def test_staff_string_method(self):
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1986-12-03', residence=house)
        person.save()
        election = Election(election_date='2018-01-01')
        election.save()
        question = BallotQuestion(question_text='Should we do that?', election=election)
        question.save()
        camp1 = Campaign(campaign_name='Yes', ballot_question=question)
        camp1.save()
        staffer = CampaignStaff(staff_memeber=person, campaign_name=camp1, position='Tester')
        self.assertEqual(str(staffer), str(person))


class GDALModelInterfaceTests(TestCase):

    def test_point_constructor_and_srs_coversion(self):
        # This will fail if there are errors in the GDAL installation
        gcoord = SpatialReference('4326')
        mycoord = SpatialReference(3857)
        trans = CoordTransform(gcoord, mycoord)
        pnt = Point(x=-122.33, y=47.61, srid=4326)
        pnt.transform(trans)


class GroupModelTests(TestCase):

    def test_create_new_group(self):
        mygroup = GroupObject(name='testgroup')
        mygroup.save()
        self.assertEqual(str(mygroup), 'testgroup')
        self.assertEqual(GroupObject.objects.count(), 1)

    def test_create_group_relation(self):
        mygroup = GroupObject(name='testgroup')
        mygroup.save()
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1986-12-03', residence=house)
        person.save()
        grouprel = GroupRelation(group=mygroup, content_object=person)
        grouprel.save()
        self.assertEqual(str(grouprel), str(person))
        grouprel2 = GroupRelation(group=mygroup, content_object=house)
        grouprel2.save()
        self.assertEqual(str(grouprel2), str(house))

    def test_multiple_group_membership(self):
        mygroup = GroupObject(name='testgroup')
        mygroup.save()
        myothergroup = GroupObject(name='secondgroup')
        myothergroup.save()
        house = Place(street_number=1, street_name='Main St.', city='Newport', state='RI')
        house.save()
        person = Person(first_name='Joe', last_name='Test', date_of_birth='1986-12-03', residence=house)
        person.save()
        grouprel = GroupRelation(group=mygroup, content_object=person)
        grouprel.save()
        otherrel = GroupRelation(group=myothergroup, content_object=person)
        otherrel.save()
        self.assertEqual(mygroup.grouprelation_set.count(), 1)
        self.assertEqual(myothergroup.grouprelation_set.count(), 1)
