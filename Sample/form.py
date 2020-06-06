from django import forms

import datetime

from .models import Sample, SampleMaterial, SampleType


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = SampleMaterial
        fields = '__all__'


class TypeForm(forms.ModelForm):
    class Meta:
        model = SampleType
        fields = '__all__'
