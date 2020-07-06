import json
import datetime
from django.db.models.query import QuerySet

from Sample.models import Sample
from Trial.models import Trials


class FilterQueryset:
    list_model = {'sample':  Sample, 'trials': Trials}
    date_field = {'sample': 'date_proc_streng__gt', 'trials': 'date_trials__gt'}

    def __init__(self, data, name_model):
        self.value_dict = {key: name for key, name in json.loads(data).items()}
        self.name_model = name_model

    def filter(self):
        if not self.value_dict:
            return self.list_model[self.name_model].objects.all()

        queryset = self.filter_date()

        if not queryset and isinstance(queryset, QuerySet):
            return queryset

        for key, value in self.value_dict.items():
            if not queryset:
                queryset = self.list_model[self.name_model].objects.filter(**{key: value})
            else:
                queryset = queryset.filter(**{key: value})

        return queryset

    def filter_date(self):
        if 'date' in self.value_dict:
            if self.value_dict['date'] == 'all':
                queryset = self.list_model[self.name_model].objects.all()
            else:
                d = datetime.date.today() - datetime.timedelta(days=int(self.value_dict['date']))
                kwargs_date = {self.date_field[self.name_model]: d}
                queryset = self.list_model[self.name_model].objects.filter(**kwargs_date)
            del self.value_dict['date']
        else:
            queryset = None
        return queryset
