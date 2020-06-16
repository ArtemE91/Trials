from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from .models import Sample, SampleType, SampleMaterial
from .filter_queryset import filter_queryset
from .form import SampleForm, MaterialForm, TypeForm

from .plotly_sample import figure


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


# _______________SAMPLE_______________________

class SampleList(ListView):
    model = Sample
    template_name = 'sample/sample.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["method"] = Sample.objects.order_by().values_list('method', flat=True).distinct()
        context["exp_param"] = Sample.objects.order_by().values_list('exp_param', flat=True).distinct()
        context["date_proc_streng"] = Sample.objects.order_by().values_list('date_proc_streng', flat=True).distinct()
        return context


class SampleTableListView(ListView):
    model = Sample
    template_name = 'sample/includes/table.html'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = filter_queryset(self.request.GET['search'])
        return queryset


class SampleDetail(AjaxableResponseMixin, DetailView):
    model = Sample
    template_name = 'sample/sample_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plot_div'] = figure()
        return context


class SampleCreate(CreateView):
    form_class = SampleForm
    template_name = 'sample/sample_create.html'
    success_url = reverse_lazy('sample:')

    def post(self, request, *args, **kwargs):
        sample_form = self.form_class(request.POST)

        if sample_form.is_valid():
            sample = sample_form.save(commit=False)
            sample.author = request.user
            sample.save()
            return redirect(sample.get_absolute_url())

        return render(request, self.template_name, {"form": sample_form})


class SampleUpdateView(UpdateView):
    form_class = SampleForm
    template_name = "sample/sample_update.html"
    success_url = reverse_lazy('sample:create')

    def get_object(self, queryset=None):
        return Sample.objects.get(id=self.kwargs['pk'])


class SampleDeleteView(DeleteView):
    model = Sample
    success_url = reverse_lazy('sample:')


# _____________________SAMPLE_MATERIAL______________________

class SampleMaterialList(ListView):
    model = SampleMaterial
    template_name = 'sample/material/material_dropdown.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = context['object_list']
        return context


class SampleMaterialDetail(AjaxableResponseMixin, DetailView):
    model = SampleMaterial
    template_name = 'sample/material/material_detail.html'


class SampleMaterialUpdateView(UpdateView):
    form_class = MaterialForm
    template_name = "sample/material/material_update.html"
    success_url = reverse_lazy('sample:material_table')

    def get_object(self, queryset=None):
        return SampleMaterial.objects.get(id=self.kwargs['pk'])


class SampleMaterialDeleteView(DeleteView):
    model = SampleMaterial
    success_url = reverse_lazy('sample:material_table')


class SampleMaterialCreate(AjaxableResponseMixin, CreateView):
    form_class = MaterialForm
    template_name = 'sample/material/material_create_modal.html'


# _____________________SAMPLE_TYPE______________________

class SampleTypeList(ListView):
    model = SampleType
    template_name = 'sample/type/type_dropdown.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = context['object_list']
        return context


class SampleTypeDetail(AjaxableResponseMixin, DetailView):
    model = SampleType
    template_name = 'sample/type/type_detail.html'


class SampleTypeUpdateView(UpdateView):
    form_class = TypeForm
    template_name = "sample/type/type_update.html"
    success_url = reverse_lazy('sample:type_table')

    def get_object(self, queryset=None):
        return SampleType.objects.get(id=self.kwargs['pk'])


class SampleTypeDeleteView(DeleteView):
    model = SampleType
    success_url = reverse_lazy('sample:type_table')


class SampleTypeCreate(AjaxableResponseMixin, CreateView):
    form_class = TypeForm
    template_name = 'sample/type/type_create_modal.html'
