from django import forms

import datetime

from .models import Sample, SampleMaterial, SampleType


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        self.fields['sample_material'].quereset = SampleMaterial.objects.all()
        self.fields['sample_type'].queryset = SampleType.objects.all()


class MaterialForm(forms.ModelForm):
    class Meta:
        model = SampleMaterial
        fields = '__all__'


class TypeForm(forms.ModelForm):
    class Meta:
        model = SampleType
        fields = '__all__'
