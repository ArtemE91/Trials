# Generated by Django 3.0.6 on 2020-06-28 15:46

import Sample.models
import Trial.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sample', '0005_sample_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedvalues',
            name='change_weight',
            field=models.FloatField(default=0, verbose_name='Масса образца после эксперимента'),
        ),
        migrations.AlterField(
            model_name='receivedvalues',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=Trial.models.ReceivedValues.experement_image_path, verbose_name='Изображение образца после эксперимента'),
        ),
        migrations.AlterField(
            model_name='receivedvalues',
            name='time_trials',
            field=models.IntegerField(default=0, verbose_name='Длительность эксперимента'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='date_proc_streng',
            field=models.DateField(blank=True, null=True, verbose_name='Дата процесса упрочнения'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='depth_coating',
            field=models.FloatField(blank=True, null=True, verbose_name='Толщина упрочнения'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='exp_param',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Параметры упрочнения'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='hardness_coating',
            field=models.FloatField(blank=True, null=True, verbose_name='Твердость упрочнения'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=Sample.models.Sample.sample_image_path, verbose_name='Внешний вид образца, начальный'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='marking',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Маркировка образца'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='method',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Способ упрочнения'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='organization',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Организация, которая провела упрочнение'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='roughness',
            field=models.FloatField(blank=True, null=True, verbose_name='Шероховатость поверхности'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='struct_coating',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Состав покрытия'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sub_hardness',
            field=models.FloatField(blank=True, null=True, verbose_name='Твердость подложки'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='weight',
            field=models.FloatField(default=0, verbose_name='Первоначальная масса образца'),
        ),
        migrations.AlterField(
            model_name='samplematerial',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Название материала образца'),
        ),
        migrations.AlterField(
            model_name='samplematerial',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип материала'),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Название типа образца'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='add_param',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительные параметры частицы'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='corner_collision',
            field=models.IntegerField(blank=True, null=True, verbose_name='Угол соударения '),
        ),
        migrations.AlterField(
            model_name='trials',
            name='date_end_trials',
            field=models.DateField(blank=True, null=True, verbose_name='Время окончания испытания'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='date_trials',
            field=models.DateField(blank=True, null=True, verbose_name='Дата проведения испытания'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='size_particle',
            field=models.IntegerField(blank=True, null=True, verbose_name='Размер частиц'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='speed_collision',
            field=models.IntegerField(blank=True, null=True, verbose_name='Скорость соударения'),
        ),
        migrations.AlterField(
            model_name='trials',
            name='type_particle',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип частицы'),
        ),
    ]
