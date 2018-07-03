from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from geopy.geocoders import Nominatim


class Place(models.Model):
    place_name = models.CharField(max_length=250, blank=True)  # optional field for place name
    street_number = models.CharField(max_length=20)
    suffix_a = models.CharField(max_length=10, blank=True)
    suffix_b = models.CharField(max_length=10, blank=True)
    street_name = models.CharField(max_length=100)
    street_address_2 = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    zip_code_4 = models.CharField(max_length=4, blank=True)

    point = models.PointField(default='POINT(0.0 0.0)')

    def geocode(self):
        geolocator = Nominatim()
        address_string = str(self.street_number) + ' ' + self.street_name + ', ' + self.city + ', ' + self.state
        location = geolocator.geocode(address_string)
        self.point.x = location.longitude
        self.point.y = location.latitude
        self.save()

    def __str__(self):
        address_string = ''
        if self.place_name:
            return self.place_name
        elif self.unit:
            address_string = address_string + self.unit + ' '
        address_string = address_string + str(self.street_number) + ' ' + self.street_name + ', ' + \
                         self.city + ', ' + self.state
        return address_string


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(blank=True)
    is_deceased = models.BooleanField(default=False)
    residence = models.ForeignKey(Place, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class ContactPhone(models.Model):
    phone_number = models.CharField(max_length=16)
    notes = models.CharField(max_length=50, blank=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    do_not_contact = models.BooleanField(default=False)


class ContactEmail(models.Model):
    email = models.EmailField()
    notes = models.CharField(max_length=50, blank=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    do_not_contact = models.BooleanField(default=False)


class MailingAddress(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    notes = models.CharField(max_length=50, blank=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    do_not_contact = models.BooleanField(default=False)


class Election(models.Model):
    election_date = models.DateField()
    election_description = models.CharField(max_length=100)

    type_choices = (
        ('PG', 'Presedential Election'),
        ('PPP', 'Presedential Preference Primary'),
        ('SG', 'Statewide General Election'),
        ('SP', 'Statewide Primary Election'),
        ('SPC', 'Special Election'),
    )
    election_type = models.CharField(max_length=3, choices=type_choices, blank=True)


class BallotQuestion(models.Model):
    question_text = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.PROTECT)

    def __str__(self):
        return self.question_text


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=250)
    ballot_question = models.ForeignKey(BallotQuestion, on_delete=models.PROTECT)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.campaign_name


class CampaignStaff(models.Model):
    campaign_name = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    staff_memeber = models.ForeignKey(Person, on_delete=models.PROTECT)
    position = models.CharField(max_length=250)

    def __str__(self):
        return str(self.staff_memeber)


class GroupObject(models.Model):
    """
    A model for grouping related objects together.  It works in conjunction with a GroupRelation object.
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)


class GroupRelationManager(models.Manager):
    # TODO: simplify and handle more complex group creation and operations
    pass

class GroupRelation(models.Model):
    group = models.ForeignKey(GroupObject, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = GroupRelationManager()

    def __str__(self):
        return str(self.content_object)
