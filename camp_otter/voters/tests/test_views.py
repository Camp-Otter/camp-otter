from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
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
        file = SimpleUploadedFile('test.csv', b'col_a, col_b \n 1,2', content_type="text/csv")
        response = self.client.post(reverse_lazy('file-upload'), {'file': file})
        self.assertContains(response, 'Success')
        #self.assertRedirects(response, reverse_lazy('success'), target_status_code=200)
