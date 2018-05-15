from django.test import TestCase
from camp_otter.voters.models import Voter

# Create your tests here.
class VoterModelTests(TestCase):

    def test_voter_str_method(self):
        voter = Voter()