from django.test import TestCase, Client
from django.urls import reverse_lazy
from camp_otter.voters.views import VoterListView


class VoterViewTests(TestCase):

    def test_voter_list_view(self):
        client = Client()
        response = client.get(reverse_lazy('voter-list'))
        self.assertEqual(response.status_code, 200)