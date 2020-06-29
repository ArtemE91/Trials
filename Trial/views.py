from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F, Q
from django.shortcuts import render

from .experiment_graph import figure, multigraf
from Sample.models import Trials, ReceivedValues, Sample
from .form import TrialForm, TrialUpdateForm, ExperementUpdateForm, ExperimentCreateForm
from .filter_queryset import filter_queryset


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        if self.request.is_ajax():
            data = {
                'pk': instance.pk,
            }
            return JsonResponse(data, status=200)
        else:
            return HttpResponseRedirect(instance.get_absolute_url())


class TrialCreate(AjaxableResponseMixin, CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'


class TrialList(ListView):
    model = Trials
    template_name = 'Trial/trials_list.html'
    search_filter = {'date_trials': 'date_trials', 'organization': 'sample__organization',
                     'marking': 'sample__marking', 'corner_collision': 'corner_collision',
                     'method': 'sample__method', 'size_particle': 'size_particle',
                     'speed_collision': 'speed_collision',
                     'material_name': 'sample__sample_material__name',
                     'material_type': 'sample__sample_material__type',
                     'type': 'sample__sample_type__name'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        for key, value in self.search_filter.items():
            context[key] = context['object_list'].order_by().values_list(value, flat=True).distinct()

        return context


class TrialTableListView(ListView):
    model = Trials
    template_name = 'trial/trial_table.html'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = filter_queryset(self.request.GET['search'])
        return queryset


class TrialDetail(DetailView):
    model = Trials
    template_name = 'Trial/trial_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_weight = self.object.sample.weight
        weight_loss = [sample_weight-experiment.change_weight for experiment in context['trials'].experiments]
        times = [experiment.time_trials for experiment in context['trials'].experiments]
        context['plot_div'] = figure(times, weight_loss)
        return context

    def get_object(self):
        trial = super(TrialDetail, self).get_object()
        trial.experiments = trial.trials_values.all().annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))
        trial.experiments = trial.experiments.order_by('time_trials')
        for e in trial.experiments:
            e.weight_loss = round(e.weight_loss, 5)
        return trial


class TrialModalDetail(DetailView):
    model = Trials
    template_name = 'Trial/trial_modal_detail.html'


class TrialDetailTr(AjaxableResponseMixin, DetailView):
    model = Trials
    template_name = 'Trial/trial_detail_tr.html'


class TrialUpdate(AjaxableResponseMixin, UpdateView):
    model = Trials
    template_name = 'Trial/trial_update.html'
    fields = '__all__'
    success_url = '/trial/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = Sample.objects.filter(Q(sample=None) | Q(id=context['trials'].sample.id))
        return context


class TrialDelete(DeleteView):
    model = Trials
    success_url = '/trial/'


class ExperimentCreate(AjaxableResponseMixin, CreateView):
    form_class = ExperimentCreateForm
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
    form_class = ExperementUpdateForm
    template_name = 'Experiment/ExperimentUpdate.html'

    def get_object(self, queryset=None):
        return ReceivedValues.objects.get(id=self.kwargs['pk'])


class TrialGraph(DetailView):
    model = Trials
    template_name = 'Trial/trial_graph.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_weight = self.object.sample.weight
        related_experiments = self.object.trials_values.all().order_by('time_trials')
        weight_loss = [sample_weight-experiment.change_weight for experiment in related_experiments]
        times = [experiment.time_trials for experiment in related_experiments]
        context['plot_div'] = figure(times, weight_loss)
        return context


def compare_graphs(request):
    sample_ids = request.GET.getlist('samples[]')
    samples = Sample.objects.filter(pk__in=sample_ids)
    related_trials = [sample.sample for sample in samples if hasattr(sample, 'sample')]
    coordinates = []
    for trial in related_trials:
        related_experiments = trial.trials_values.all().order_by('time_trials')
        weight_loss = [trial.sample.weight-experiment.change_weight for experiment in related_experiments]
        times = [experiment.time_trials for experiment in related_experiments]
        graph_name = 'Испытание:' + str(trial.sample)
        coordinates.append((times, weight_loss, graph_name))
    graph = multigraf(coordinates)
    return render(request, 'Experiment/CompareGraphs.html', {'plot_div': graph})
