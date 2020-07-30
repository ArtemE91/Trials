from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Modification(models.Model):
    """ Информация по упрочнению """
    method = models.CharField(max_length=255, blank=True, null=True, verbose_name='Способ упрочнения')
    exp_param = models.CharField(max_length=255, blank=True, null=True, verbose_name='Параметры упрочнения')
    depth_coating = models.FloatField(blank=True, null=True, verbose_name='Толщина упрочнения')
    hardness_coating = models.FloatField(blank=True, null=True, verbose_name='Твердость упрочнения')
    organization = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name='Организация, которая провела упрочнение')
    struct_coating = models.CharField(max_length=255, blank=True, null=True, verbose_name='Состав покрытия')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Автор записи')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'modification'

    def __str__(self):
        return f'{self.method}'

    @staticmethod
    def get_absolute_url():
        return reverse('modification:list')

