from django.db import models
from django.core.validators import RegexValidator


class Place(models.Model):
    place_name = models.CharField(max_length=250, blank=True)  # optional field for place name
    unit = models.CharField(max_length=10, blank=True)
    street_address = models.CharField(max_length=100)
    street_address_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        address_string = ''
        if self.place_name:
            return self.place_name
        elif self.unit:
            address_string = address_string + self.unit + ' '
        address_string = address_string + self.street_address + ', ' + self.city + ', ' + self.state
        return address_string


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    residence = models.ForeignKey(Place, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class ContactPhone(models.Model):
    phone_number = models.CharField(max_length=16)
    notes = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)


class ContactEmail(models.Model):
    email = models.EmailField()
    notes = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)


class Election(models.Model):
    election_date = models.DateField()


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
