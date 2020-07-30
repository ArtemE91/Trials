from django import forms

from .models import Modification


class ModificationForm(forms.ModelForm):
    class Meta:
        model = Modification
        fields = ['method', 'exp_param', 'depth_coating', 'hardness_coating', 'organization', 'struct_coating']
        labels = {
            'method': 'Способ упрочнения',
            'exp_param': 'Параметры упрочнения',
            'depth_coating': 'Толщина упрочнения',
            'hardness_coating': 'Твердость упрочнения',
            'organization': 'Организация, которая провела упрочнение',
            'struct_coating': 'Состав покрытия',
        }