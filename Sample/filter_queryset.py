import json
import datetime

from .models import Sample

'''Выбираем все не пустые фильтры'''
'''Приводим к необходимому формату для запроса в бд'''
'''Первый фильтр делает запрос в бд остальные фильтруют пришедший queryset'''


def filter_queryset(data):
    value_dict = {key: name for key, name in json.loads(data).items()}
    print(value_dict)

    if 'date_proc_streng__in' in value_dict:
        date_format = []
        for date in value_dict['date_proc_streng__in']:
            date_format.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
        value_dict['date_proc_streng__in'] = date_format

    if not value_dict:
        return Sample.objects.all()

    queryset = None

    for key, value in value_dict.items():
        if not queryset:
            queryset = Sample.objects.filter(**{key: value})
        else:
            queryset = queryset.filter(**{key: value})

    return queryset
