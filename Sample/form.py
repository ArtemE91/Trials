from django import forms

import datetime

from .models import Sample


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'

    # def clean_tags(self):
    #     new_data = self.cleaned_data['date_proc_streng']
    #     new_data = datetime.datetime.strptime(new_data, '%Y-%m-%d').date()
    #
    #     return new_data
