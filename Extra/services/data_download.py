import xlwt
import datetime

from django.core.exceptions import ObjectDoesNotExist

from User.models import User
from Sample.models import Sample
from Trial.models import ReceivedValues

""" Поля моделей для записи в excel"""
fields = {
    'sample': ['method', 'exp_param', 'date_proc_streng', 'depth_coating',
               'roughness', 'hardness_coating', 'struct_coating', 'sub_hardness',
               'organization', 'weight', 'marking', 'description', 'author', 'date_create'],
    'material': ['name', 'type', 'description', 'author', 'date_create'],
    'type': ['name', 'author', 'date_create'],
    'trial': ['size_particle', 'speed_collision', 'add_param', 'corner_collision',
              'date_trials', 'date_end_trials', 'type_particle', 'description',
              'author', 'date_create'],
    'experiment': ['time_trials', 'change_weight', 'author', 'date_create']
}


def get_verbose_name(model, field):
    verbose_name = field
    try:
        verbose_name = model._meta.get_field(field).verbose_name
    finally:
        return verbose_name


def get_str_attribute(model, field):
    str_attr = ''
    try:
        attr = model.__getattribute__(field)
        if isinstance(attr, User):
            str_attr = attr.username
        elif isinstance(attr, datetime.datetime):
            str_attr = attr.strftime("%m-%d-%Y, %H:%M:%S")
        elif isinstance(attr, datetime.date):
            str_attr = attr.strftime("%m-%d-%Y")
        else:
            str_attr = attr
    finally:
        return str_attr


def excel(ids):

    wb = xlwt.Workbook(encoding='utf-8')

    sheet = 1

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    sheets = Sample.objects.filter(pk__in=ids)

    for sample in sheets:
        ws = wb.add_sheet(f'{sheet} образец')
        col_num = 0  # нулевой столбец
        sheet += 1

        # Название столбцов и их значения для Образцов
        for field in fields['sample']:
            attr = get_str_attribute(sample, field)
            if attr:
                row_num = 0    # 1 Строка в документе
                verbose = get_verbose_name(sample, field)
                ws.write(row_num, col_num, verbose, font_style)    # Имя столбца
                row_num += 1    # Опускаем строку на один
                ws.write(row_num, col_num, attr, font_style)    # Значение стоблца
                col_num += 1    # Столбец вправо на один

        col_num = 0  # возращаем столбец на нулевое значение

        try:
            if sample.sample_material:
                for field in fields['material']:
                    attr = get_str_attribute(sample.sample_material, field)
                    if attr:
                        row_num = 3  # 3 строка в документе
                        verbose = get_verbose_name(sample.sample_material, field)
                        ws.write(row_num, col_num, verbose, font_style)
                        row_num += 1
                        ws.write(row_num, col_num, attr, font_style)
                        col_num += 1
        except ObjectDoesNotExist as e:
            pass

        col_num += 1  # Увеличиваем столбец на один, тип пишем в теже строки что и материал

        try:
            if sample.sample_type:
                for field in fields['type']:
                    attr = get_str_attribute(sample.sample_type, field)
                    if attr:
                        row_num = 3  # 3 строка в документе
                        verbose = get_verbose_name(sample.sample_type, field)
                        ws.write(row_num, col_num, verbose, font_style)
                        row_num += 1
                        ws.write(row_num, col_num, attr, font_style)
                        col_num += 1
        except ObjectDoesNotExist as e:
            pass

        col_num = 0

        try:
            if sample.sample:
                for field in fields['trial']:
                    attr = get_str_attribute(sample.sample, field)
                    if attr:
                        row_num = 6  # 6 строка в документе
                        verbose = get_verbose_name(sample.sample, field)
                        ws.write(row_num, col_num, verbose, font_style)
                        row_num += 1
                        ws.write(row_num, col_num, attr, font_style)
                        col_num += 1
        except ObjectDoesNotExist as e:
            pass

        col_num = 0

        try:
            related_experiments = sample.sample.trials_values.all().order_by('time_trials')
        except ObjectDoesNotExist as e:
            related_experiments = None

        if related_experiments:
            for field in fields['experiment']:  # Заполняем название столбцов
                row_num = 9  # 9 строка в документе
                verbose = get_verbose_name(ReceivedValues, field)
                ws.write(row_num, col_num, verbose, font_style)
                col_num += 1
            for exp in related_experiments:  # Заполняем аттрибуты
                col_num = 0
                row_num += 1
                for field in fields['experiment']:
                    ws.write(row_num, col_num, get_str_attribute(exp, field), font_style)
                    col_num += 1

    return wb
