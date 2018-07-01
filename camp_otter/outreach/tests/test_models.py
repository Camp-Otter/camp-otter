from django.test import TestCase
from camp_otter.outreach.models import OutreachList


class OutreachListModelTests(TestCase):

    def test_empty_outreach_list_object_create(self):
        mylist = OutreachList(list_name='My Test List')
        mylist.save()
        self.assertEqual(OutreachList.objects.get(list_name='My Test List').list_name, 'My Test List')
