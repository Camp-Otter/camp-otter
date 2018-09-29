from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from camp_otter.voters.views import VoterListView

from .testdata.dummy_data import UPLOADED_VOTER_LIST_CSV_DATA


class VoterViewTests(TestCase):

    def test_voter_list_view(self):
        client = Client()
        response = client.get(reverse_lazy('voter-list'))
        self.assertEqual(response.status_code, 200)

    def test_voter_detail_view_voter_does_not_exist(self):
        client = Client()
        response = client.get(reverse_lazy('voter-detail', kwargs={'pk': 1}, current_app='voters'))
        self.assertEqual(response.status_code, 404)

    def test_file_upload_view(self):
        client = Client()
        response = client.get(reverse_lazy('voter-upload'))
        self.assertEqual(response.status_code, 200)

    def test_file_upload_post(self):
        file = SimpleUploadedFile('test.csv', UPLOADED_VOTER_LIST_CSV_DATA, content_type="text/csv")
        client = Client()
        response = client.post(reverse_lazy('voter-upload'), {'file': file})
        self.assertRedirects(response, reverse_lazy('success'), target_status_code=200)
