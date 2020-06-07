from django import forms
from Sample.models import Trials, Sample


class TrialForm(forms.ModelForm):
    class Meta:
        model = Trials
        fields = '__all__'
        labels = {
            'size_particle': 'Размер частицы',
            'speed_collision': 'Cкорость столкновения',
            'add_param': 'Параметры'
            }

    def __init__(self, *args, **kwargs):
        super(TrialForm, self).__init__(*args, **kwargs)
        self.fields['add_param'].widget.attrs['placeholder'] = 'return false;'
        self.fields['sample'].queryset = Sample.objects.filter(sample=None)
