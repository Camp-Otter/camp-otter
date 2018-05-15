from django.db import models
from camp_otter.core.models import Person

# Create your models here.
class Voter(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.person)
