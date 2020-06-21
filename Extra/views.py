import yaml
import json

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.db import transaction

from Sample.models import Sample, SampleMaterial, SampleType, Trials, ReceivedValues


class DataLoading:
    author = 'author_id'
    data_write = {'sample_type': {},
                  'sample_material': {},
                  'sample': {},
                  'trials': {},
                  'experiment': {}}
    error_message = {'block': '', 'error_message': ''}

    def __init__(self, config, author_id):
        try:
            self.author_id = author_id
            self.sample_type = config['sample_type']
            self.sample_material = config['sample_material']
            self.sample = config['sample']
            self.trial = config['trials']
            self.experiment = config['received_values']
        except Exception as e:
            self.error_message['block'] = 'Не заполнены основные поля в файле для загрузки данных.' \
                                          ' Ознакомтесь с инструкцией заполнения!'
            self.error_message['error_message'] = e

    def write_data(self):
        try:
            self.save_type()
            self.save_material()
            self.save_sample()
            self.save_trial()
            self.save_experiment()
            return self.data_write
        except ValueError as e:
            self.error_message['error_message'] = e
            return self.error_message

    def save_type(self):
        try:
            for type_id in self.sample_type:
                self.error_message['block'] = json.dumps(self.sample_type[type_id])
                self.sample_type[type_id][self.author] = self.author_id
                try:
                    self.data_write['sample_type'][type_id] = SampleType.objects.get(**self.sample_type[type_id])
                except ObjectDoesNotExist:
                    self.data_write['sample_type'][type_id] = SampleType.objects.create(**self.sample_type[type_id])
        except Exception as e:
            raise ValueError(e)

    def save_material(self):
        try:
            for material_id in self.sample_material:
                self.error_message['block'] = json.dumps(self.sample_material[material_id])
                self.sample_material[material_id][self.author] = self.author_id
                try:
                    self.data_write['sample_material'][material_id] = SampleMaterial.objects.get(
                        **self.sample_material[material_id])
                except ObjectDoesNotExist:
                    self.data_write['sample_material'][material_id] = SampleMaterial.objects.create(
                        **self.sample_material[material_id])
        except Exception as e:
            raise ValueError(e)

    def save_sample(self):
        try:
            for sample_id in self.sample:
                self.error_message['block'] = json.dumps(self.sample[sample_id])
                self.sample[sample_id][self.author] = self.author_id

                id_material = self.data_write['sample_material'][self.sample[sample_id]['sample_material_id']].id
                self.sample[sample_id]['sample_material_id'] = id_material

                id_type = self.data_write['sample_type'][self.sample[sample_id]['sample_type_id']].id
                self.sample[sample_id]['sample_type_id'] = id_type

                self.data_write['sample'][sample_id] = Sample.objects.create(**self.sample[sample_id])
        except Exception as e:
            raise ValueError(e)

    def save_trial(self):
        try:
            for trials_id in self.trial:
                self.error_message['block'] = json.dumps(self.trial[trials_id])
                self.trial[trials_id][self.author] = self.author_id

                sample_id = self.data_write['sample'][self.trial[trials_id]['sample_id']].id
                self.trial[trials_id]['sample_id'] = sample_id

                self.data_write['trials'][trials_id] = Trials.objects.create(**self.trial[trials_id])
        except Exception as e:
            raise ValueError(e)

    def save_experiment(self):
        try:
            for exp_id in self.experiment:
                self.error_message['block'] = json.dumps(self.experiment[exp_id])
                self.experiment[exp_id][self.author] = self.author_id

                trials_id = self.data_write['trials'][self.experiment[exp_id]['trials_id']].id
                self.experiment[exp_id]['trials_id'] = trials_id

                self.data_write['experiment'][exp_id] = ReceivedValues.objects.create(**self.experiment[exp_id])
        except Exception as e:
            raise ValueError(e)


class DataLoadingTemplateView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'extra/data_loading.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # В дальнейшем сделать проверку на размер файла
        try:
            config = yaml.safe_load(request.FILES['file'].read())
        except Exception as e:
            context = {'value': 'Ошибка в чтении файла! Проверьте формат файла.',
                       'error': e}
        else:
            data_loading = DataLoading(config, request.user.id)
            data = data_loading.write_data()
            if 'error_message' in data:
                context = {'title': 'Блок в котором возникли ошибки: ',
                           'value': data['block'], 'error': data['error_message']}
            else:
                context = {'sample': data['sample'], 'trials': data['trials'],
                           'experiment': data['experiment']}
        finally:
            return render(request, self.template_name, context)
