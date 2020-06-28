# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.shortcuts import reverse
from django.conf import settings


class AbstractModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SampleType(AbstractModel):
    """Тип образца"""
    name = models.CharField(max_length=255, verbose_name='Название типа образца', default='')

    class Meta:
        db_table = 'sample_type'

    def __str__(self):
        return f'{self.name}'

    # Добавил для AjaxableResponseMixin, для реализции DetailView необходиму возращать url элемента
    @staticmethod
    def get_absolute_url():
        return reverse('sample:type_table')


class SampleMaterial(AbstractModel):
    """Материал из которого изготовлен образец"""
    name = models.CharField(max_length=255, verbose_name='Название материала образца', default='')
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип материала')
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'sample_material'
        ordering = ['name', 'type']

    def __str__(self):
        label = ''
        if self.name:
            label += self.name + " "
        if self.type:
            label += self.type
        return label

    @staticmethod
    def get_absolute_url():
        return reverse('sample:material_table')


class Sample(AbstractModel):
    """Информация по образцу"""
    def sample_image_path(self, filename):
        return f"sample/{self.id}/{filename}"

    method = models.CharField(max_length=255, blank=True, null=True, verbose_name='Способ упрочнения')
    exp_param = models.CharField(max_length=255, blank=True, null=True, verbose_name='Параметры упрочнения')
    date_proc_streng = models.DateField(blank=True, null=True, verbose_name='Дата процесса упрочнения')
    depth_coating = models.FloatField(blank=True, null=True, verbose_name='Толщина упрочнения')
    roughness = models.FloatField(blank=True, null=True, verbose_name='Шероховатость поверхности')
    hardness_coating = models.FloatField(blank=True, null=True, verbose_name='Твердость упрочнения')
    struct_coating = models.CharField(max_length=255, blank=True, null=True, verbose_name='Состав покрытия')
    sub_hardness = models.FloatField(blank=True, null=True, verbose_name='Твердость подложки')
    organization = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name='Организация, которая провела упрочнение')
    weight = models.FloatField(verbose_name='Первоначальная масса образца', default=0)
    marking = models.CharField(max_length=255, blank=True, null=True, verbose_name='Маркировка образца')
    image = models.FileField(upload_to=sample_image_path, null=True, blank=True,
                             verbose_name='Внешний вид образца, начальный')
    description = models.TextField(blank=True, null=True)

    sample_material = models.ForeignKey(SampleMaterial, blank=True, null=True,
                                        on_delete=models.CASCADE, related_name='material')
    sample_type = models.ForeignKey(SampleType, blank=True, null=True,
                                    on_delete=models.CASCADE, related_name='type')

    class Meta:
        db_table = 'sample'

    def get_absolute_url(self):
        return reverse('sample:detail', kwargs={'pk': self.pk})

    def get_image(self):
        if not self.image:
            return f'{settings.MEDIA_URL}/default.png'
        return f'{settings.MEDIA_URL}/{self.image}'

    def __str__(self):
        label = f'{self.sample_material.name}'
        if self.sample_material.type:
            label += f'_{self.sample_material.type}'
        if self.method:
            label += f'_{self.method}'
        if self.marking:
            label += f'_{self.marking}'
        return label


class Trials(AbstractModel):
    """Информация по испытанию"""
    size_particle = models.IntegerField(blank=True, null=True, verbose_name='Размер частиц')
    speed_collision = models.IntegerField(blank=True, null=True, verbose_name='Скорость соударения')
    add_param = models.CharField(max_length=255, blank=True, null=True, verbose_name='Дополнительные параметры частицы')
    corner_collision = models.IntegerField(blank=True, null=True, verbose_name='Угол соударения ')
    date_trials = models.DateField(blank=True, null=True, verbose_name='Дата проведения испытания')
    date_end_trials = models.DateField(blank=True, null=True, verbose_name='Время окончания испытания')
    type_particle = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип частицы')
    description = models.TextField(blank=True, null=True)

    sample = models.OneToOneField(Sample, blank=True, null=True, on_delete=models.CASCADE, related_name='sample')

    class Meta:
        db_table = 'trials'

    def get_absolute_url(self):
        return reverse('trial:detail', kwargs={'pk': self.pk})


class ReceivedValues(AbstractModel):
    """Информация по эксперементу"""
    def experement_image_path(self, filename):
        return f"experement/trial_{self.trials.id}/{filename}"

    change_weight = models.FloatField(verbose_name='Масса образца после эксперимента', default=0)
    time_trials = models.IntegerField(verbose_name='Длительность эксперимента', default=0)
    image = models.FileField(upload_to=experement_image_path, null=True, blank=True,
                             verbose_name='Изображение образца после эксперимента')

    trials = models.ForeignKey(Trials, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="trials_values")

    class Meta:
        db_table = 'received_values'

    @staticmethod
    def get_absolute_url():
        return reverse('trial:list')
