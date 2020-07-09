from django.views.generic import TemplateView
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse

from .services import data_loading, data_download


class DataLoadingTemplateView(TemplateView):
    """ Загрузка данных в базу из yml файла """
    http_method_names = ['get', 'post']
    template_name = 'extra/data_loading.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = data_loading.get_data_load_context(request)
        return render(request, self.template_name, context)


class InfoFIllTemplateView(TemplateView):
    """ Информация по заполнению yml конфига"""
    http_method_names = ['get']
    template_name = 'extra/info.html'


class DownloadDataTemplateView(TemplateView):
    """ Выгрузка данных из базы в excel"""
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        sample_ids = request.GET.getlist('samples[]')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="trials.xls"'
        wb = data_download.excel(sample_ids)

        wb.save(response)
        return response



