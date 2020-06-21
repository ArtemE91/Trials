from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from Sample.models import Trials, ReceivedValues
from .experiment_graph import figure
from .form import TrialForm, TrialUpdateForm, ExperementForm
from django.http import JsonResponse
from django.db.models import F


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        instanse = form.save(commit=False)
        instanse.author = self.request.user
        instanse.save()
        if self.request.is_ajax():
            data = {
                'pk': instanse.pk,
            }
            return JsonResponse(data, status=200)
        else:
            return super().form_valid(form)


class TrialCreate(AjaxableResponseMixin, CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'


class TrialList(ListView):
    model = Trials
    template_name = 'Trial/trials_list.html'


class TrialDetail(DetailView):
    model = Trials
    template_name = 'Trial/trial_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_weight = self.object.sample.weight
        weight_loss = [sample_weight-experiment.change_weight for experiment in self.object.trials_values.all()]
        times = [experiment.time_trials for experiment in self.object.trials_values.all()]
        context['plot_div'] = figure(times, weight_loss)
        return context

    def get_object(self):
        trial = super(TrialDetail, self).get_object()
        trial.experiments = trial.trials_values.all().annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))
        trial.experiments = trial.experiments.order_by('-weight_loss')
        for e in trial.experiments:
            e.weight_loss = round(e.weight_loss, 5)
        return trial


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


class ExperimentCreate(AjaxableResponseMixin, CreateView):
    form_class = ExperementForm
    template_name = 'Experiment/Experiment.html'


class ExperimentDelete(AjaxableResponseMixin, DeleteView):
    model = ReceivedValues
    success_url = '/trial/'


class ExperimentList(ListView):
    model = ReceivedValues
    template_name = 'Experiment/ExperimentTable.html'

    def get_queryset(self):
        trial_pk = self.kwargs['pk']
        trial = Trials.objects.get(pk=trial_pk)
        qset = trial.trials_values.all()
        return qset.annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))


class ExperimentUpdate(AjaxableResponseMixin, UpdateView):
    model = ReceivedValues
    template_name = 'Experiment/ExperimentUpdate.html'
    fields = '__all__'

class TrialGraph(DetailView):
    model = Trials
    template_name = 'Trial/trial_graph.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_weight = self.object.sample.weight
        weight_loss = [sample_weight-experiment.change_weight for experiment in self.object.trials_values.all()]
        times = [experiment.time_trials for experiment in self.object.trials_values.all()]
        context['plot_div'] = figure(times, weight_loss)
        return context
