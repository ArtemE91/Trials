from django.views.generic import TemplateView

from django.shortcuts import render
from django.db import transaction

from .services import data_loading


class DataLoadingTemplateView(TemplateView):
    """ Загрузка данных в базу из yml файла """
    http_method_names = ['get', 'post']
    template_name = 'extra/data_loading.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = data_loading.get_data_load_context(request)
        return render(request, self.template_name, context)
