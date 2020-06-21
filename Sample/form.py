from django import forms

import datetime

from .models import Sample, SampleMaterial, SampleType


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['method', 'exp_param', 'date_proc_streng', 'depth_coating', 'roughness',
                  'hardness_coating', 'struct_coating', 'sub_hardness', 'organization',
                  'weight', 'marking', 'sample_material', 'sample_type']
        labels = {
            'method': 'Cпособ упрочнения / нанесения покрытия',
            'exp_param': 'Параметры упрочнения (воздействие было) / нанесения покрытия',
            'date_proc_streng': 'Дата процесса',
            'depth_coating': 'Толщина покрытия / глубина упрочнения, [мкм]',
            'roughness': 'Шероховатость поверхности после модификации, [мкм]',
            'hardness_coating': 'Твердость покрытия / упрочнения, [HV]',
            'struct_coating': 'Состав покрытия',
            'sub_hardness': 'Твердость подложки, [HB]',
            'organization': 'Организация, которая провела упрочнение',
            'weight': 'Первоначальная масса, [г]',
            'marking': 'Маркировка',
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
        fields = ['name', 'type', 'description']
        labels = {
            'name': 'Название',
            'type': 'Тип',
            'description': 'Описание',
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = SampleType
        fields = ['name']
        labels = {
            'name': 'Название',
        }
