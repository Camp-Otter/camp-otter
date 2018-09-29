from django.views.generic.list import ListView
from django.views.generic import View, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from camp_otter.core.models import Place
from camp_otter.voters.models import Voter
from camp_otter.voters.forms import UploadVoterFileForm, UploadHistoryFileForm, VoterForm
from camp_otter.voters.utilities import import_uploaded_voter_file_to_db, load_uploaded_file_to_dataframe, import_voter_list_dataframe, import_voter_history_dataframe


# Create your views here.
def success(request):
    return render(request, 'voters/success.html')


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voters/voter_detail.html'


class VoterListView(ListView):
    model = Voter
    paginate_by = 100  # the number of voters shown per page
    template_name = 'voters/voter_list.html'

    def get_queryset(self):
        return Voter.objects.order_by('person__last_name', 'person__first_name')


class CreateVoterView(FormView):
    model = Voter
    form_class = VoterForm
    template_name = "voters/voter_form.html"

    def form_valid(self, form):
        # build objects with required fields first

        residence = Place.objects.get_or_create(
            street_number=form.cleaned_data['street_number'],
            street_name=form.cleaned_data['street_name'],
            city=form.cleaned_data['city'],
            state=form.cleaned_data['state'],
            zip_code=form.cleaned_data['zip']
        )
        # then handle optional fields

        residence = residence[0]
        residence.save()

        voter = Voter.objects.create_new_voter(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            residence=residence,
            date_of_birth=form.cleaned_data['date_of_birth'],
            voter_id=form.cleaned_data['voter_id']
        )
        voter.save()
        return redirect('voter-detail', pk=voter.pk)

# Upload view based on https://www.andygoldschmidt.com/2014/09/10/django-file-uploads-with-class-based-views/
class VoterFileUploadView(View):
    form_class = UploadVoterFileForm
    success_url = reverse_lazy('success')
    template_name = 'voters/voter_file_upload.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # TODO: render a table with a preview of the uploaded file to allow selection of columns
            # build data dictionary from form input

            data_dict = {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'voter_id': form.cleaned_data['voter_id'],
                        'voter_status': form.cleaned_data['voter_status'],
                        'date_of_birth': form.cleaned_data['date_of_birth'],
                        'street_number': form.cleaned_data['street_number'],
                        'street_name': form.cleaned_data['street_name'],
                        'street_name_2': form.cleaned_data['street_name_2'],
                        'suffix_a': form.cleaned_data['suffix_a'],
                        'suffix_b': form.cleaned_data['suffix_b'],
                        'unit': form.cleaned_data['unit'],
                        'city': form.cleaned_data['city'],
                        'state': form.cleaned_data['state'],
                        'zip': form.cleaned_data['zip'],
                        }

            required_fields = ['first_name',  # fields to verify are complete
                               'last_name',
                               'voter_id',
                               'street_number',
                               'street_name',
                               'city',
                               'state',
                               'zip']
            df = load_uploaded_file_to_dataframe(request.FILES['file'], data_dict)
            import_voter_list_dataframe(df.dropna(subset=required_fields))
            return redirect(self.success_url)  # TODO: render file in preprocessing view
        else:
            return render(request, self.template_name, {'form': form})


class HistoryFileUploadView(View):
    form_class = UploadHistoryFileForm
    success_url = reverse_lazy('success')
    template_name = 'voters/history_file_upload.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # TODO: render a table with a preview of the uploaded file to allow selection of columns
            # build data dictionary from form input

            data_dict = {
                        'voter_id': form.cleaned_data['voter_id'],
                        'date': form.cleaned_data['election_date'],
                        'election': form.cleaned_data['election_description'],
                        'precinct': form.cleaned_data['voter_precinct'],
                        }
            df = load_uploaded_file_to_dataframe(request.FILES['file'], data_dict)
            import_voter_history_dataframe(df.dropna())
            return redirect(self.success_url)  # TODO: render file in preprocessing view
        else:
            return render(request, self.template_name, {'form': form})