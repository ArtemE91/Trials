# Generated by Django 3.0.6 on 2020-07-30 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sample', '0008_auto_20200730_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='depth_coating',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='exp_param',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='hardness_coating',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='method',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='struct_coating',
        ),
    ]
