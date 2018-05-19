from django.views.generic.list import ListView

from camp_otter.voters.models import Voter


# Create your views here.
class VoterListView(ListView):
    model = Voter
    paginate_by = 1
    template_name = 'voter_list.html'
