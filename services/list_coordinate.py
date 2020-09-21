from Sample.models import Sample
from django.db.models import F, Q, QuerySet
from Trial.models import Trials
import math
import numpy as np
from typing import Union, List, Tuple, Optional
import json

TYPE_1 = 1
TYPE_2 = 2
TYPE_3 = 3
TYPE_POLYNOMIAL = (TYPE_1, TYPE_2, TYPE_3)


class Trace:

    def __init__(self, x: list, y: list, name: str, mode: str, ) -> None:
        self.x = x
        self.y = y
        self.name = name
        self.mode = mode

    @classmethod
    def create_trace_first(cls, trial: Trials):

        x, y, name = cls.first_coordinate_grid(trial)
        trace = cls(x=x, y=y, name=name, mode='markers')
        return trace

    @classmethod
    def create_trace_second(cls, trial: Trials):
        x, y, name = cls.second_coordinate_grid(trial)
        trace = cls(x=x, y=y, name=name, mode='markers')
        return trace

    @classmethod
    def first_coordinate_grid(cls, trial: Trials) -> Optional[Tuple[list, list, str]]:
        data_experiment = cls.get_data_experiment(trial)

        y = [0] + [round(value['weight_loss'], 5) for value in data_experiment]
        x = [0] + [value['time_trials'] for value in data_experiment]

        return x, y, str(trial.sample)

    @classmethod
    def second_coordinate_grid(cls, trial: Trials) -> Optional[Tuple[list, list, str]]:
        data_experiment = cls.get_data_experiment(trial)

        x = cls.calculate_x_for_second_cg(data_experiment, trial)
        y = cls.calculate_y_for_second_cg(data_experiment, trial)

        return x, y, str(trial.sample)

    @staticmethod
    def calculate_x_for_second_cg(data_experiment: QuerySet, trial: Trials) -> list:
        x = [0]
        for i_block in data_experiment:
            try:
                denominator = trial.sample_density * trial.size_particle * trial.droplets_distance
                average_depth = round(i_block['weight_loss'], 5) / denominator
                x.append(average_depth)
            except (ZeroDivisionError, TypeError):
                return []
            except KeyError:
                return []
        return x

    @classmethod
    def calculate_y_for_second_cg(cls, data_experiment: QuerySet, trial: Trials) -> list:
        """Расчет значений средней глубины эрозионного износа"""
        y = [0]

        try:
            numerator = cls.get_numerator_amount_of_liquid(trial)
            for i_block in data_experiment:
                denominator = trial.size_particle * trial.sample_erosion_height
                average_depth = (numerator * i_block['time_trials']) / denominator
                y.append(average_depth)
        except (ZeroDivisionError, TypeError):
            return []
        except KeyError:
            return []

        return y

    @staticmethod
    def get_numerator_amount_of_liquid(trial: Trials) -> int:
        """Расчет числителя для формулы глубины эрозийного износа без аргумента ti(время эксперимента)"""
        try:
            first_arg = (math.pi * (trial.size_particle ** 3)) / 6
            second_arg = trial.sample_erosion_height / trial.droplets_distance
            third_arg = trial.speed_collision / (math.pi * trial.samples_distance_diameter)

            numerator = first_arg * trial.water_density * second_arg * trial.number_of_droplet_flow * third_arg
        except (ZeroDivisionError, TypeError):
            raise ZeroDivisionError
        except KeyError:
            raise KeyError

        return numerator

    @staticmethod
    def get_data_experiment(trial: Trials) -> QuerySet:
        experiment_list = trial.trials_values.all().order_by('time_trials')
        params_experiment = experiment_list.annotate(weight_loss=F('trials__sample__weight') - F('change_weight'))
        data = params_experiment.values('weight_loss', 'change_weight', 'time_trials')

        return data

    def as_dict(self):
        return dict(x=self.x, y=self.y, name=self.name, mode=self.mode)

    def __bool__(self):
        return False if not(self.x or self.y) else True


trace1 = Trace.create_trace_first
trace2 = Trace.create_trace_second

list_trace = {1: trace1, 2: trace2}


def get_list_coordinate_new(sample_ids: list) -> dict:
    # 1. Получаем Trials
    # 2. Группируем их
    # 3. Получаем Trace для каждого элемента в группе
    # 4. Отправляем List[Trace] полученный в пункте 3 для получения полиномов
    related_trials = Trials.objects.filter(sample__pk__in=sample_ids)
    grouped_trials = group_by_material(related_trials)
    trials_info = []
    for trial in grouped_trials:
        trial_group_info = {'traces': {}, 'trend_lines': {}}
        for coordinate_grid, func_trace in list_trace.items():
            trial_group_info['traces'][coordinate_grid] = []
            trace = func_trace(trial.get())
            if trace:
                trial_group_info['traces'][coordinate_grid].append(trace)
        for coordinate_grid, _ in list_trace.items():
            if trial_group_info['traces'][coordinate_grid]:
                trial_group_info['trend_lines'] = create_trend_traces(trial_group_info['traces'][coordinate_grid],
                                                                      coordinate_grid)
    print(trial_group_info)


def create_trend_traces(trial_group_info, coordinate_grid):
    trend_traces = {coordinate_grid: {}}
    for type_pol in TYPE_POLYNOMIAL:
        trend_traces[coordinate_grid][type_pol] = []
        trend_traces[coordinate_grid][type_pol].append(TracePolynomial.create_trace(trial_group_info, type_pol))
    return trend_traces


def get_list_coordinate(sample_ids: list) -> dict:
    related_trials = Trials.objects.filter(sample__pk__in=sample_ids)
    grouped_trials = group_by_material(related_trials)
    trials_info = []
    for trial_group in grouped_trials:
        trial_group_info = {'traces': [], 'trend_lines': []}
        for trial in trial_group:
            trace = create_trace(trial)
            if trace:
                trial_group_info['traces'].append(trace)
        if trial_group_info['traces']:
            related_trials_info = [[t.pk, str(t.sample)] for t in
                                   trial_group]  # Пока не понял как сделать через values или values_list
            trial_group_info['trend_lines'] = get_trend_traces(trial_group_info['traces'], related_trials_info)
            trials_info.append(trial_group_info)
    all_traces = []
    trend_ids = []
    for ti in trials_info:
        all_traces += ti['traces']
        trend_ids.append(list(range(len(all_traces), len(all_traces) + len(ti['trend_lines']))))
        all_traces += ti['trend_lines']
    return {'traces': all_traces, 'trend_ids': group_trend_ids(trend_ids)}


def create_trace(trial):
    related_experiments = trial.trials_values.all().order_by('time_trials')
    if not related_experiments:
        return {}
    weight_loss = [round(trial.sample.weight - experiment.change_weight, 5)
                   for experiment in related_experiments]
    weight_loss.insert(0, 0)
    times = [experiment.time_trials for experiment in related_experiments]
    times.insert(0, 0)
    trace = {
        'x': times,
        'y': weight_loss,
        'name': str(trial.sample),
        'mode': 'markers'
    }
    return trace


def get_trend_traces(traces, related_trials_info):
    union_times = list(sum([trace['x'] for trace in traces], []))
    union_times.sort()
    time_no_duplicates = sorted(list(set(union_times)))
    union_weights = []
    for time in time_no_duplicates:
        for trace in traces:
            if time in trace['x']:
                index = trace['x'].index(time)
                weight = trace['y'][index]
                union_weights.append(weight)
    trend_traces = []
    for deg in [3, 2, 1]:
        poly_trend, function_name, function_equation = calculate_poly_trend(union_times, union_weights, deg)
        times = list(dict.fromkeys(union_times))
        trend_trace = {
            'x': times,
            'y': poly_trend,
            'mode': 'lines+markers',
            'name': function_name,
            'text': function_equation,
            'related_trials': list(related_trials_info)
        }
        trend_traces.append(trend_trace)
    return trend_traces


def calculate_poly_trend(x, y, deg=2):
    p = np.polyfit(x, y, deg)
    x = list(dict.fromkeys(x))
    function_name = f'Полином {deg} степени'
    trend_values = [np.polyval(p, i) for i in x]
    return trend_values, function_name, str(np.poly1d(p))


def group_trend_ids(trend_ids):
    if not trend_ids:
        return []
    trends_count = len(trend_ids[0])
    grouped = []
    for i in range(trends_count):
        group = [l[i] for l in trend_ids]
        grouped.append(group)
    return grouped


def calculate_linear_approximation(x, y):
    p = np.polyfit(x, y, 1)
    x0 = -p[1] / p[0]
    x_list = [x0, x[-1]]
    y_list = [0, p[0] * x[-1] + p[1]]
    return x_list, y_list


def group_by_material(trials):
    grouped_trials = []
    if len(trials) == 1:
        return [trials]
    '''Для образцов типа «грибок», у которых не указан способ упрочнения'''
    gribok_unmodified_trials = trials.filter(sample__sample_type__name='грибок',
                                             sample__modification__isnull=True)
    for q in gribok_unmodified_trials:
        if any([q in sub_qs for sub_qs in grouped_trials]):
            continue
        filtered = gribok_unmodified_trials.filter(sample__sample_type=q.sample.sample_type,
                                                   sample__sample_material__name=q.sample.sample_material.name,
                                                   sample__sample_material__type=q.sample.sample_material.type,
                                                   sample__sub_hardness=q.sample.sub_hardness,
                                                   size_particle=q.size_particle,
                                                   speed_collision=q.speed_collision,
                                                   corner_collision=q.corner_collision,
                                                   type_particle=q.type_particle,
                                                   flow_type=q.flow_type,
                                                   chamber_pressure=q.chamber_pressure)
        grouped_trials.append(filtered)
    trials = trials.exclude(id__in=gribok_unmodified_trials)
    '''Для образцов типа «грибок», у которых указан способ упрочнения'''
    gribok_modified_trials = trials.filter(sample__sample_type__name='грибок',
                                           sample__modification__isnull=False)
    for q in gribok_modified_trials:
        if any([q in sub_qs for sub_qs in grouped_trials]):
            continue
        filtered = gribok_modified_trials.filter(sample__sample_type=q.sample.sample_type,
                                                 sample__sample_material__name=q.sample.sample_material.name,
                                                 sample__sample_material__type=q.sample.sample_material.type,
                                                 sample__sub_hardness=q.sample.sub_hardness,
                                                 sample__modification=q.sample.modification,
                                                 size_particle=q.size_particle,
                                                 speed_collision=q.speed_collision,
                                                 corner_collision=q.corner_collision,
                                                 type_particle=q.type_particle,
                                                 flow_type=q.flow_type,
                                                 chamber_pressure=q.chamber_pressure)
        grouped_trials.append(filtered)
    trials = trials.exclude(id__in=gribok_modified_trials)
    '''Для образцов типа «диск» или «пластина», у которых не указан способ упрочнения'''
    disk_plast_unmod_trials = trials.filter(sample__sample_type__name__in=['диск', 'пластина'],
                                            sample__modification__isnull=True)
    for q in disk_plast_unmod_trials:
        if any([q in sub_qs for sub_qs in grouped_trials]):
            continue
        filtered = disk_plast_unmod_trials.filter(sample__sample_type=q.sample.sample_type,
                                                  sample__sample_material__name=q.sample.sample_material.name,
                                                  sample__sample_material__type=q.sample.sample_material.type,
                                                  sample__sub_hardness=q.sample.sub_hardness,
                                                  size_particle=q.size_particle,
                                                  speed_collision=q.speed_collision,
                                                  corner_collision=q.corner_collision,
                                                  type_particle=q.type_particle,
                                                  abrasive_type=q.abrasive_type,
                                                  sample_temp=q.sample_temp,
                                                  air_consumption=q.air_consumption,
                                                  abrasive_consumption=q.abrasive_consumption,
                                                  nozzle_diam=q.nozzle_diam,
                                                  distance_sub=q.distance_sub)
        grouped_trials.append(filtered)
    trials = trials.exclude(id__in=disk_plast_unmod_trials)
    '''Для образцов типа «диск» или «пластина», у которых указан способ упрочнения'''
    disk_plast_modif_trials = trials.filter(sample__sample_type__name__in=['диск', 'пластина'],
                                            sample__modification__isnull=False)
    for q in disk_plast_modif_trials:
        if any([q in sub_qs for sub_qs in grouped_trials]):
            continue
        filtered = disk_plast_modif_trials.filter(sample__sample_type=q.sample.sample_type,
                                                  sample__sample_material__name=q.sample.sample_material.name,
                                                  sample__sample_material__type=q.sample.sample_material.type,
                                                  sample__sub_hardness=q.sample.sub_hardness,
                                                  sample__modification=q.sample.modification,
                                                  size_particle=q.size_particle,
                                                  speed_collision=q.speed_collision,
                                                  corner_collision=q.corner_collision,
                                                  type_particle=q.type_particle,
                                                  sample_temp=q.sample_temp,
                                                  air_consumption=q.air_consumption,
                                                  abrasive_consumption=q.abrasive_consumption,
                                                  abrasive_type=q.abrasive_type,
                                                  nozzle_diam=q.nozzle_diam,
                                                  distance_sub=q.distance_sub)
        grouped_trials.append(filtered)
    trials = trials.exclude(id__in=disk_plast_modif_trials)
    return grouped_trials


class TracePolynomial:

    def __init__(self, x: list, y: list, name: str, mode: str, related_trials: list, text: str, **kwargs) -> None:
        self.x = x
        self.y = y
        self.name = name
        self.mode = mode
        self.related_trials = related_trials
        self.text = text

    @classmethod
    def create_trace(cls, traces: List[Trace], type_polynomial: int):
        union_times = list(sum([trace.x for trace in traces], []))
        union_times.sort()
        time_no_duplicates = sorted(list(set(union_times)))
        union_weights = []
        for time in time_no_duplicates:
            for trace in traces:
                if time in trace.x:
                    index = trace.x.index(time)
                    weight = trace.y[index]
                    union_weights.append(weight)

        poly_trend, function_name, function_equation = calculate_poly_trend(union_times, union_weights, type_polynomial)
        times = list(dict.fromkeys(union_times))

        trend_trace = cls(x=times, y=poly_trend, mode='lines+markers', name=function_name,
                          text=function_equation, related_trials=['id', 'name'])

        return trend_trace
