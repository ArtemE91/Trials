# Generated by Django 3.0.6 on 2020-09-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trial', '0004_auto_20200819_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiveddata',
            name='polynomial_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип полинома'),
        ),
    ]