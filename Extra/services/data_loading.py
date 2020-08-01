import yaml
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist

from Sample.models import Sample, SampleMaterial, SampleType
from Trial.models import Trials, ReceivedValues
from Modification.models import Modification


class DataLoading:
    author = 'author_id'
    data_write = {'sample_type': {},
                  'sample_material': {},
                  'modification': {},
                  'sample': {},
                  'trials': {},
                  'experiment': {}}
    error_message = {'block': '', 'error_message': ''}

    def __init__(self, config, author_id, image):
        try:
            self.author_id = author_id
            self.sample_type = config['sample_type']
            self.sample_material = config['sample_material']
            if 'modification' in config:
                self.modification = config['modification']
            else:
                self.modification = None
            self.sample = config['sample']
            self.trial = config['trials']
            self.experiment = config['received_values']
            self.image = image
        except Exception as e:
            self.error_message['block'] = 'Не заполнены основные поля в файле для загрузки данных.' \
                                          ' Ознакомтесь с инструкцией заполнения!'
            self.error_message['error_message'] = e

    def write_data(self):
        try:
            self.save_type()
            self.save_material()
            self.save_modification()
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

    def save_modification(self):
        try:
            if self.modification:
                for modification_id in self.modification:
                    self.error_message['block'] = json.dumps(self.modification[modification_id])
                    self.modification[modification_id][self.author] = self.author_id
                    try:
                        self.data_write['modification'][modification_id] = Modification.objects.get(
                            **self.modification[modification_id])
                    except ObjectDoesNotExist:
                        self.data_write['modification'][modification_id] = Modification.objects.create(
                            **self.modification[modification_id])
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

                if 'modification_id' in self.sample[sample_id]:
                    id_modification = self.data_write['modification'][self.sample[sample_id]['modification_id']].id
                    self.sample[sample_id]['modification_id'] = id_modification

                if 'image' in self.sample[sample_id]:
                    self.sample[sample_id]['image'] = self.search_image(self.sample[sample_id]['image'])

                if 'date_proc_streng' in self.sample[sample_id]:
                    date = self.sample[sample_id]['date_proc_streng']
                    self.sample[sample_id]['date_proc_streng'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()

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

                if 'date_trials' in self.trial[trials_id]:
                    date = self.trial[trials_id]['date_trials']
                    self.trial[trials_id]['date_trials'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()

                if 'date_end_trials' in self.trial[trials_id]:
                    date = self.trial[trials_id]['date_end_trials']
                    self.trial[trials_id]['date_end_trials'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()

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

                if 'image' in self.experiment[exp_id]:
                    self.experiment[exp_id]['image'] = self.search_image(self.experiment[exp_id]['image'])

                self.data_write['experiment'][exp_id] = ReceivedValues.objects.create(**self.experiment[exp_id])
        except Exception as e:
            raise ValueError(e)

    def search_image(self, name_file):
        for file in self.image:
            if name_file == file.name:
                self.image.remove(file)
                return file
        return None


def get_data_load_context(request):
    try:
        config = yaml.safe_load(request.FILES['file'].read())
        image_list = request.FILES.getlist('image')
    except Exception as e:
        context = {'value': 'Ошибка в чтении файла! Проверьте формат файла.',
                   'error': e}
    else:
        data_loading = DataLoading(config, request.user.id, image_list)
        data = data_loading.write_data()
        if 'error_message' in data:
            context = {'title': 'Блок в котором возникли ошибки: ',
                       'value': data['block'], 'error': data['error_message']}
        else:
            context = {'sample': data['sample'], 'trials': data['trials'],
                       'experiment': data['experiment']}
    finally:
        return context
