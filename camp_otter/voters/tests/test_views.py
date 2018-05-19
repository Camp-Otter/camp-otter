from django.test import TestCase, Client
from django.urls import reverse_lazy
from camp_otter.voters.views import VoterListView


class VoterViewTests(TestCase):

    def test_voter_list_view(self):
        client = Client()
        response = client.get(reverse_lazy('voter-list'))
        self.assertEqual(response.status_code, 200)

    def test_file_upload_view(self):
        client = Client()
        response = client.get(reverse_lazy('file-upload'))
        self.assertEqual(response.status_code, 200)

    def test_file_upload_post(self):
        client = Client()
        response = client.post(reverse_lazy('file-upload'), data={'title': 'Title', 'file': 'abcd'})
        self.assertRedirects(response, reverse_lazy('success'), status_code=302, target_status_code=200)
