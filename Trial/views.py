from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from Sample.models import Trials
from .form import TrialForm, TrialUpdateForm, ExperementForm
from django.http import JsonResponse


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data, status=200)
        else:
            return response


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


class TrialModalDetail(DetailView):
    model = Trials
    template_name = 'Trial/trial_modal_detail.html'


class TrialDetailTr(AjaxableResponseMixin, DetailView):
    model = Trials
    template_name = 'Trial/trial_detail_tr.html'


class TrialUpdate(UpdateView):
    model = Trials
    template_name = 'Trial/trial_update.html'
    fields = '__all__'
    success_url = '/trial/'


class TrialDelete(DeleteView):
    model = Trials
    success_url = '/trial/'


class ExperimentCreate(CreateView):
    form_class = ExperementForm
    template_name = 'Experiment/Experiment.html'
