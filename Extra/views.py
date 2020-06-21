import os
import yaml

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from Sample.models import Sample, SampleMaterial, SampleType, Trials, ReceivedValues


class DataLoading:
    author = 'author_id'
    data_write = {'sample_type': {},
                  'sample_material': {},
                  'sample': {},
                  'trials': {}}

    def __init__(self, config, author_id):
        self.author_id = author_id
        self.sample_type = config['sample_type']
        self.sample_material = config['sample_material']
        self.sample = config['sample']
        self.trial = config['trials']
        self.experiment = config['received_values']

    def write_data(self):
        self.save_type()
        self.save_material()
        self.save_sample()
        self.save_trial()
        self.save_experiment()

    def save_type(self):
        for type_id in self.sample_type:
            self.sample_type[type_id][self.author] = self.author_id
            try:
                self.data_write['sample_type'][type_id] = SampleType.objects.get(**self.sample_type[type_id]).id
            except ObjectDoesNotExist:
                self.data_write['sample_type'][type_id] = SampleType.objects.create(**self.sample_type[type_id]).id

    def save_material(self):
        for material_id in self.sample_material:
            self.sample_material[material_id][self.author] = self.author_id
            try:
                self.data_write['sample_material'][material_id] = SampleMaterial.objects.get(
                    **self.sample_material[material_id]).id
            except ObjectDoesNotExist:
                self.data_write['sample_material'][material_id] = SampleMaterial.objects.create(
                    **self.sample_material[material_id]).id

    def save_sample(self):
        for sample_id in self.sample:
            self.sample[sample_id][self.author] = self.author_id

            id_material = self.data_write['sample_material'][self.sample[sample_id]['sample_material_id']]
            self.sample[sample_id]['sample_material_id'] = id_material

            id_type = self.data_write['sample_type'][self.sample[sample_id]['sample_type_id']]
            self.sample[sample_id]['sample_type_id'] = id_type

            self.data_write['sample'][sample_id] = Sample.objects.create(**self.sample[sample_id]).id

    def save_trial(self):
        for trials_id in self.trial:
            self.trial[trials_id][self.author] = self.author_id

            sample_id = self.data_write['sample'][self.trial[trials_id]['sample_id']]
            self.trial[trials_id]['sample_id'] = sample_id

            self.data_write['trials'][trials_id] = Trials.objects.create(**self.trial[trials_id]).id

    def save_experiment(self):
        for exp_id in self.experiment:
            self.experiment[exp_id][self.author] = self.author_id

            trials_id = self.data_write['trials'][self.experiment[exp_id]['trials_id']]
            self.experiment[exp_id]['trials_id'] = trials_id

            ReceivedValues.objects.create(**self.experiment[exp_id])


class DataLoadingTemplateView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'extra/data_loading.html'

    def post(self, request, *args, **kwargs):
        # В дальниешем сделать проверку на размер файла
        config = yaml.safe_load(request.FILES['file'].read())
        data_loading = DataLoading(config, request.user.id)
        return redirect(request.path)