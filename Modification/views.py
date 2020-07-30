from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Modification
from .form import ModificationForm
from services.mixin import AjaxableResponseMixin


class ModificationListView(LoginRequiredMixin, ListView):
    model = Modification
    template_name = 'modification/modification_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modification'] = context['object_list']
        return context


class ModificationDetailView(LoginRequiredMixin, DetailView):
    model = Modification
    template_name = 'modification/modification_detail.html'


class ModificationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ModificationForm
    template_name = 'modification/modification_update.html'
    success_url = reverse_lazy('modification:list')

    def get_object(self, queryset=None):
        return Modification.objects.get(id=self.kwargs['pk'])


class ModificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Modification
    success_url = reverse_lazy('modification:list')


class ModificationCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    form_class = ModificationForm
    template_name = 'modification/modification_create.html'
