from django import forms
from Sample.models import Trials, Sample, ReceivedValues


class TrialForm(forms.ModelForm):
    class Meta:
        model = Trials
        fields = ['size_particle', 'speed_collision', 'add_param', 'corner_collision',
                  'date_trials', 'date_end_trials', 'type_particle', 'description', 'sample']
        labels = {
            'size_particle': 'Размер частицы',
            'speed_collision': 'Cкорость столкновения',
            'add_param': 'Параметры'
            }

    def __init__(self, *args, **kwargs):
        super(TrialForm, self).__init__(*args, **kwargs)
        self.fields['add_param'].widget.attrs['placeholder'] = 'Нужны ли плейсхолдеры?'
        self.fields['sample'].queryset = Sample.objects.filter(sample=None)
        self.fields['sample'].widget.attrs['class'] = 'ui fluid search dropdown'


class TrialUpdateForm(forms.ModelForm):
    class Meta:
        model = Trials
        fields = '__all__'


class ExperementForm(forms.ModelForm):
    class Meta:
        model = ReceivedValues
        fields = ['change_weight', 'time_trials', 'image', 'trials']
