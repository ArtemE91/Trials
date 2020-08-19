from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.db.models import F, Q
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .experiment_graph import figure, multigraf
from .models import Trials, ReceivedValues, Sample
from .form import TrialForm, ExperimentForm
from services.mixin import AjaxableResponseMixin
from services.list_coordinate import get_list_coordinate
from services.filter_queryset import FilterQueryset


class TrialCreate(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'


class TrialList(LoginRequiredMixin, ListView):
    model = Trials
    template_name = 'Trial/trials_list.html'
    search_filter = {'date_trials': 'date_trials', 'organization': 'sample__modification__organization',
                     'marking': 'sample__marking', 'corner_collision': 'corner_collision',
                     'method': 'sample__modification__method', 'size_particle': 'size_particle',
                     'speed_collision': 'speed_collision',
                     'material_name': 'sample__sample_material__name',
                     'material_type': 'sample__sample_material__type',
                     'type': 'sample__sample_type__name', 'flow_type': 'flow_type',
                     'chamber_pressure': 'chamber_pressure', 'sample_temp': 'sample_temp',
                     'abrasive_type': 'abrasive_type', 'air_consumption': 'air_consumption',
                     'abrasive_consumption': 'abrasive_consumption', 'nozzle_diam': 'nozzle_diam',
                     'distance_sub': 'distance_sub'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        for key, value in self.search_filter.items():
            context[key] = context['object_list'].order_by().values_list(value, flat=True).distinct()

        return context


class TrialTableListView(LoginRequiredMixin, ListView):
    model = Trials
    template_name = 'Trial/trial_table.html'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        date_filter = FilterQueryset(self.request.GET['search'], 'trials')
        queryset = date_filter.filter()
        return queryset


class TrialDetail(LoginRequiredMixin, DetailView):
    model = Trials
    template_name = 'Trial/trial_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_id = self.object.sample.id
        context['traces'] = get_list_coordinate([sample_id])['traces']
        return context

    def get_object(self):
        trial = super(TrialDetail, self).get_object()
        trial.experiments = trial.trials_values.all().annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))
        trial.experiments = trial.experiments.order_by('time_trials')
        for e in trial.experiments:
            e.weight_loss = round(e.weight_loss, 5)
        return trial


class TrialModalDetail(LoginRequiredMixin, DetailView):
    model = Trials
    template_name = 'Trial/trial_modal_detail.html'


class TrialDetailTr(LoginRequiredMixin, AjaxableResponseMixin, DetailView):
    model = Trials
    template_name = 'Trial/trial_detail_tr.html'


class TrialUpdate(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    form_class = TrialForm
    template_name = 'Trial/trial_update.html'
    success_url = '/trial/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = Sample.objects.filter(Q(sample=None) | Q(id=context['trials'].sample.id))
        return context

    def get_object(self, queryset=None):
        return Trials.objects.get(id=self.kwargs['pk'])


class TrialDelete(LoginRequiredMixin, DeleteView):
    model = Trials
    success_url = '/trial/'


class ExperimentCreate(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    form_class = ExperimentForm
    template_name = 'Experiment/Experiment.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trial = Trials.objects.get(pk=self.kwargs['pk'])
        ctx['trial'] = trial
        return ctx

    def get_form(self, **kwargs):
        form = super().get_form()
        form.instance.trials = Trials.objects.get(pk=self.kwargs['pk'])
        return form


class ExperimentDelete(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    model = ReceivedValues
    success_url = '/trial/'


class ExperimentList(LoginRequiredMixin, ListView):
    model = ReceivedValues
    template_name = 'Experiment/ExperimentTable.html'

    def get_queryset(self):
        trial_pk = self.kwargs['pk']
        trial = Trials.objects.get(pk=trial_pk)
        qset = trial.trials_values.all()
        return qset.annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))


class ExperimentUpdate(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    form_class = ExperimentForm
    template_name = 'Experiment/ExperimentUpdate.html'

    def get_object(self, queryset=None):
        return ReceivedValues.objects.get(id=self.kwargs['pk'])


class CompareGraphsTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'Experiment/CompareGraphs.html'

    def get(self, request, *args, **kwargs):
        sample_ids = request.GET.getlist('samples[]')
        return render(request, 'Experiment/CompareGraphs.html', {'sample_ids': sample_ids})


class AjaxCompareGraphs(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        sample_ids = request.GET.getlist('samples[]')
        coordinates = get_list_coordinate(sample_ids)
        return JsonResponse(coordinates, status=200)
