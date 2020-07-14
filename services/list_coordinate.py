from Sample.models import Sample
from Trial.models import Trials
import numpy as np


""" 
list = {'data':
    {
     'coordinates': [ (times, weights, name), (times1, weights1, name) ],
     'poly_trend1': [times, weights, function_str]
    },
    {
     'coordinates': [(times, weight, name)]
    }
}
"""
def get_list_coordinate(sample_ids: list) -> dict:
    related_trials = Trials.objects.filter(sample__pk__in=sample_ids)
    grouped_trials = group_by_material(related_trials)
    trials_info = []
    for trial_group in grouped_trials:
        trial_group_info = {'coordinates': []}
        for trial in trial_group:
            related_experiments = trial.trials_values.all().order_by('time_trials')
            weight_loss = [round(trial.sample.weight - experiment.change_weight, 5) for experiment in related_experiments]
            times = [experiment.time_trials for experiment in related_experiments]
            trial_group_info['coordinates'].append((times, weight_loss, str(trial.sample)))
        trials_info.append(trial_group_info)
        if len(trial_group) > 1:
            trials_info = add_trend_line_info(trials_info)
    return {'data': trials_info}


def add_trend_line_info(trials_info):
    for trial_group in trials_info:
        coordinates = trial_group['coordinates']
        if len(coordinates) > 1:
            union_times = list(sum([c[0] for c in coordinates], []))
            union_times.sort()
            union_weights = []
            time_no_duplicates = sorted(list(set(union_times)))
            for time in time_no_duplicates:
                for c in coordinates:
                    if time in c[0]:
                        index = c[0].index(time)
                        weight = c[1][index]
                        union_weights.append(weight)
            poly_trend, function = calculate_poly_trend(union_times, union_weights, 3)
            times = list(dict.fromkeys(union_times))
            trial_group['poly_trend'] = [times, poly_trend, function]
    return trials_info


def calculate_poly_trend(x, y, deg=2):
    p = np.polyfit(x, y, deg)
    x = list(dict.fromkeys(x))
    if deg == 1:
        return [p[0]*x+p[1] for x in x], 'Полином 1 степени' #f'{p[0]}*x+{p[1]}'
    if deg == 2:
        return [p[0]*x**2+p[1]*x+p[2] for x in x], 'Полином 2 степени' #f'{p[0]}*x^2+{p[1]}*x+{p[2]}'
    if deg == 3:
        return [p[0]*x**3+p[1]*x**2+p[2]*x+p[3] for x in x], "Полином 3 степени" #f'{p[0]}*x^3+{p[1]}*x^2+{p[2]}*x+{p[3]}'


def group_by_material(trials):
    ''' Разбиваю QuerySet на список QuerySet-ов с выбранными одинаковыми полями '''
    grouped_trials = []
    for q in trials:
        if any([q in sub_qs for sub_qs in grouped_trials]):
            continue
        filtered_trials = trials.filter(sample__sample_material=q.sample.sample_material, 
                                        size_particle=q.size_particle, 
                                        speed_collision=q.speed_collision,
                                        corner_collision=q.corner_collision)
        grouped_trials.append(filtered_trials)
    return grouped_trials
