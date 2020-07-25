from django.db import models
from Sample.models import AbstractModel, Sample
from django.shortcuts import reverse


class Trials(AbstractModel):
    """Информация по испытанию"""
    size_particle = models.IntegerField(blank=True, null=True, verbose_name='Размер частиц')
    speed_collision = models.IntegerField(blank=True, null=True, verbose_name='Скорость соударения')
    add_param = models.CharField(max_length=255, blank=True, null=True, verbose_name='Дополнительные параметры частицы')
    corner_collision = models.IntegerField(blank=True, null=True, verbose_name='Угол соударения ')
    date_trials = models.DateField(blank=True, null=True, verbose_name='Дата проведения испытания')
    date_end_trials = models.DateField(blank=True, null=True, verbose_name='Время окончания испытания')
    type_particle = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип частицы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    flow_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип потока')
    chamber_pressure = models.CharField(max_length=255, blank=True, null=True, verbose_name='Давление в камере')
    sample_temp = models.CharField(max_length=255, blank=True, null=True, verbose_name='Температура образца')
    abrasive_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип абразива')
    air_consumption = models.CharField(max_length=255, blank=True, null=True, verbose_name='Расход воздуха')
    abrasive_consumption = models.CharField(max_length=255, blank=True, null=True, verbose_name='Расход абразива')
    nozzle_diam = models.CharField(max_length=255, blank=True, null=True, verbose_name='Диаметр сопла')
    distance_sub = models.CharField(max_length=255, blank=True, null=True, verbose_name='Расстояние от сопла до образца')

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
