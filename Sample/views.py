from django.views.generic import ListView, DetailView, CreateView, View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Sample, SampleType, SampleMaterial
from .filter_queryset import filter_queryset
from .form import SampleForm, MaterialForm, TypeForm


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


class SampleDetail(DetailView):
    model = Sample
    template_name = 'sample/sample_detail.html'
    pk_url_kwarg = "id"


class SampleCreate(AjaxableResponseMixin, CreateView):
    form_class = SampleForm
    template_name = 'sample/sample_create.html'


class SampleMaterialList(ListView):
    model = SampleMaterial
    template_name = 'sample/material/material.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = context['object_list']
        return context


class SampleMaterialCreate(AjaxableResponseMixin, CreateView):
    form_class = MaterialForm
    template_name = 'sample/material/material_create.html'


class SampleTypeList(ListView):
    model = SampleType
    template_name = 'sample/type/type.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = context['object_list']
        return context


class SampleTypeCreate(AjaxableResponseMixin, CreateView):
    form_class = TypeForm
    template_name = 'sample/type/type_create.html'
