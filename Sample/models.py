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
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sample_type'

    def __str__(self):
        return f'{self.name}'

    # Добавил для AjaxableResponseMixin, для реализции DetailView необходиму возращать url элемента
    def get_absolute_url(self):
        return reverse('sample:type_table')


class SampleMaterial(AbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'sample_material'

    def __str__(self):
        label = ''
        if self.name:
            label += self.name + " "
        if self.type:
            label += self.type + " "
        if self.description:
            label += self.description
        return label

    def get_absolute_url(self):
        return reverse('sample:material_table')


class Sample(AbstractModel):

    def sample_image_path(self, filename):
        return f"sample/{self.id}/{filename}"

    method = models.CharField(max_length=255, blank=True, null=True)
    exp_param = models.CharField(max_length=255, blank=True, null=True)
    date_proc_streng = models.DateField(blank=True, null=True)
    depth_coating = models.FloatField(blank=True, null=True)
    roughness = models.FloatField(blank=True, null=True)
    hardness_coating = models.FloatField(blank=True, null=True)
    struct_coating = models.CharField(max_length=255, blank=True, null=True)
    sub_hardness = models.FloatField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    marking = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to=sample_image_path, null=True, blank=True)

    sample_material = models.ForeignKey(SampleMaterial, on_delete=models.CASCADE,
                                        blank=True, null=True, related_name='material')
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='type')

    class Meta:
        db_table = 'sample'

    def get_absolute_url(self):
        return reverse('sample:detail', kwargs={'pk': self.pk})

    def get_image(self):
        if not self.image:
            return f'{settings.MEDIA_URL}/default.png'
        return f'{settings.MEDIA_URL}/{self.image}'


class Trials(AbstractModel):
    size_particle = models.IntegerField(blank=True, null=True)
    speed_collision = models.IntegerField(blank=True, null=True)
    add_param = models.CharField(max_length=255, blank=True, null=True)
    corner_collision = models.IntegerField(blank=True, null=True)
    date_trials = models.DateField(blank=True, null=True)
    date_end_trials = models.DateField(blank=True, null=True)
    type_particle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE,
                                  blank=True, null=True, related_name='sample')

    class Meta:
        db_table = 'trials'


class ReceivedValues(AbstractModel):
    change_weight = models.FloatField(blank=True, null=True)
    time_trials = models.IntegerField(blank=True, null=True)
    image = models.FileField(upload_to=None, null=True, blank=True)

    trials = models.ForeignKey(Trials, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="trials_values")

    class Meta:
        db_table = 'received_values'

    def get_absolute_url(self):
        return reverse('trial:list')