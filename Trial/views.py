from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from Sample.models import Trials
from .form import TrialForm, TrialUpdateForm


class TrialCreate(CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'


class TrialList(ListView):
    model = Trials
    template_name = 'Trial/trials_list.html'


class TrialDetail(DetailView):
    model = Trials
    template_name = 'Trial/trial_detail.html'


class TrialUpdate(UpdateView):
    model = Trials
    template_name = 'Trial/trial_update.html'
    fields = '__all__'
    success_url = '/trial/'


class TrialDelete(DeleteView):
    model = Trials
    # template_name = 'Trial/trial_delete.html'
    success_url = '/trial/'
