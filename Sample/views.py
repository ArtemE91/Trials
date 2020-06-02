from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import render

from .models import Sample
from .filter_queryset import filter_queryset
from .form import SampleForm


def home(request):
    return render(request, 'sample/sample.html')


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


class SampleCreate(CreateView):
    form_class = SampleForm
    template_name = 'sample/sample_create.html'

