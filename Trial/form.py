from django import forms
from Sample.models import Trials, Sample, ReceivedValues


class TrialForm(forms.ModelForm):
    class Meta:
        model = Trials
        fields = ['size_particle', 'speed_collision', 'add_param', 'corner_collision',
                  'date_trials', 'date_end_trials', 'type_particle', 'description', 'sample']
        labels = {
            'size_particle': 'Размер частицы',
            'speed_collision': 'Cкорость соударения',
            'add_param': 'Параметры',
            'corner_collision': 'Угол соударения',
            'date_trials': 'Дата начала испытаний',
            'date_end_trials': 'Дата окончания испытаний',
            'type_particle': 'Тип частиц',
            'description': 'Описание параметров работы стенда',
            'sample': 'Образец'
            }

    def __init__(self, *args, **kwargs):
        super(TrialForm, self).__init__(*args, **kwargs)
        # self.fields['add_param'].widget.attrs['placeholder'] = 'Нужны ли плейсхолдеры?'
        self.fields['sample'].queryset = Sample.objects.filter(sample=None)
        self.fields['sample'].widget.attrs['class'] = 'ui fluid search dropdown'


class TrialUpdateForm(forms.ModelForm):
    class Meta:
        model = Trials
        fields = '__all__'


class ExperementUpdateForm(forms.ModelForm):
    class Meta:
        model = ReceivedValues
        fields = ['change_weight', 'time_trials', 'image']


class ExperimentCreateForm(forms.ModelForm):
    class Meta:
        model = ReceivedValues
        fields = ['change_weight', 'time_trials', 'image']

        labels = {
            'change_weight': 'Масса после испытания',
            'time_trials': 'Время испытания',
            'image': 'Изображение образца',
        }

