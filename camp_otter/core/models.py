from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .postgis_utilities import tiger_geocode_address, pretty_address


class Place(models.Model):
    place_name = models.CharField(max_length=250, blank=True)  # optional field for place name
    street_number = models.CharField(max_length=20)
    suffix_a = models.CharField(max_length=20, blank=True)
    suffix_b = models.CharField(max_length=20, blank=True)
    street_name = models.CharField(max_length=100)
    street_name_2 = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=30)
    zip_code_4 = models.CharField(max_length=4, blank=True)

    point = models.PointField(default='POINT(0.0 0.0)')

    def pretty_address(self):
        # https://postgis.net/docs/Normalize_Address.html
        pretty_addy = ''  # start with blank string
        pretty_addy += str(self.street_number) + ' '
        pretty_addy += self.street_name + ', '
        if self.street_name_2:
            pretty_addy += self.street_name_2 + ', '
        if self.suffix_a:
            pretty_addy += 'Unit ' + self.suffix_a + ', '
        if self.suffix_b:
            pretty_addy += 'Unit ' + self.suffix_b + ', '
        if self.unit:
            pretty_addy += 'Unit ' + self.unit + ', '
        pretty_addy += self.city + ', '
        pretty_addy += self.state + ', '
        pretty_addy += self.zip_code
        if self.zip_code_4:
            pretty_addy += '-' + self.zip_code_4

        return pretty_address('tiger', pretty_addy)

    def geocode(self):
        # TODO: need to log this and provide an update bar for batch jobs
        db = 'tiger'
        geo_data = tiger_geocode_address(db, self.pretty_address())
        self.point.x = geo_data[1]
        self.point.y = geo_data[2]
        self.save()

    def __str__(self):
        if self.place_name:
            return self.place_name
        else:
            return self.pretty_address()


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
