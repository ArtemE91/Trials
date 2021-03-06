# Generated by Django 3.0.6 on 2020-06-16 15:36

import Sample.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('change_weight', models.FloatField(blank=True, null=True)),
                ('time_trials', models.IntegerField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to=None)),
            ],
            options={
                'db_table': 'received_values',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('method', models.CharField(blank=True, max_length=255, null=True)),
                ('exp_param', models.CharField(blank=True, max_length=255, null=True)),
                ('date_proc_streng', models.DateField(blank=True, null=True)),
                ('depth_coating', models.FloatField(blank=True, null=True)),
                ('roughness', models.FloatField(blank=True, null=True)),
                ('hardness_coating', models.FloatField(blank=True, null=True)),
                ('struct_coating', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_hardness', models.FloatField(blank=True, null=True)),
                ('organization', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('marking', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to=Sample.models.Sample.sample_image_path)),
            ],
            options={
                'db_table': 'sample',
            },
        ),
        migrations.CreateModel(
            name='SampleMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sample_material',
            },
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'sample_type',
            },
        ),
        migrations.CreateModel(
            name='Trials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('size_particle', models.IntegerField(blank=True, null=True)),
                ('speed_collision', models.IntegerField(blank=True, null=True)),
                ('add_param', models.CharField(blank=True, max_length=255, null=True)),
                ('corner_collision', models.IntegerField(blank=True, null=True)),
                ('date_trials', models.DateField(blank=True, null=True)),
                ('date_end_trials', models.DateField(blank=True, null=True)),
                ('type_particle', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'trials',
            },
        ),
    ]
