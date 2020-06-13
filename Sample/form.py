from django import forms

import datetime

from .models import Sample, SampleMaterial, SampleType


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        labels = {
            'method': 'Cпособ',
            'exp_param': 'Параметры',
            'date_proc_streng': 'Дата процесса',
            'depth_coating': 'Толщина',
            'roughness': 'Шероховатость поверхности',
            'hardness_coating': 'Твердость',
            'struct_coating': 'Состав покрытия',
            'sub_hardness': 'Твердость подложки',
            'organization': 'Организация которая провела упрочнение',
            'weight': 'Первоначальная масса',
            'sample_material': 'Материал',
            'sample_type': 'Тип'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sample_material'].quereset = SampleMaterial.objects.all()
        self.fields['sample_type'].queryset = SampleType.objects.all()


class MaterialForm(forms.ModelForm):
    class Meta:
        model = SampleMaterial
        fields = '__all__'
        labels = {
            'name': 'Название',
            'type': 'Тип',
            'description': 'Описание',
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = SampleType
        fields = '__all__'
        labels = {
            'name': 'Название',
        }
