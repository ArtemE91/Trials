import json
import datetime

from .models import Sample


def filter_queryset(data):
    value_dict = {key: name for key, name in json.loads(data).items()}

    if not value_dict:
        return Sample.objects.all()

    if 'date_proc_streng__in' in value_dict:
        date_format = []
        for date in value_dict['date_proc_streng__in']:
            date_format.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
        value_dict['date_proc_streng__in'] = date_format

    queryset = None

    if 'date' in value_dict:
        if value_dict['date'] == 'all':
            queryset = Sample.objects.all()
        else:
            d = datetime.date.today() - datetime.timedelta(days=int(value_dict['date']))
            queryset = Sample.objects.filter(date_proc_streng__gt=d)
        del value_dict['date']

    for key, value in value_dict.items():
        if not queryset:
            queryset = Sample.objects.filter(**{key: value})
        else:
            queryset = queryset.filter(**{key: value})

    return queryset