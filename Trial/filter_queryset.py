import json
import datetime

from Sample.models import Trials


def filter_queryset(data):
    value_dict = {key: name for key, name in json.loads(data).items()}

    if not value_dict:
        return Trials.objects.all()

    if 'date_trials' in value_dict:
        date_format = []
        for date in value_dict['date_trials']:
            date_format.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
        value_dict['date_trials'] = date_format

    queryset = None

    if 'date' in value_dict:
        if value_dict['date'] == 'all':
            queryset = Trials.objects.all()
        else:
            d = datetime.date.today() - datetime.timedelta(days=int(value_dict['date']))
            queryset = Trials.objects.filter(date_trials__gt=d)
        del value_dict['date']

    for key, value in value_dict.items():
        if not queryset:
            queryset = Trials.objects.filter(**{key: value})
        else:
            queryset = queryset.filter(**{key: value})

    return queryset