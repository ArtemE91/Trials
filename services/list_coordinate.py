from Sample.models import Sample
from Trial.models import Trials
import numpy as np


""" 
list = {'data':
    {
     'coordinates': [ (times, weights, name), (times1, weights1, name) ],
     'poly_trend': [times, weights, function_str]
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
            weight_loss.insert(0, 0)
            times = [experiment.time_trials for experiment in related_experiments]
            times.insert(0, 0)
            trial_group_info['coordinates'].append((times, weight_loss, str(trial.sample)))
        trials_info.append(trial_group_info)
        trials_info = add_trend_line_info(trials_info)
    return {'data': trials_info}


def add_trend_line_info(trials_info):
    for trial_group in trials_info:
        coordinates = trial_group['coordinates']
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
        x = [0, x[-1]]
        return [p[0]*x+p[1] for x in x], 'Полином 1 степени' #f'{p[0]}*x+{p[1]}'
    if deg == 2:
        return [p[0]*x**2+p[1]*x+p[2] for x in x], 'Полином 2 степени' #f'{p[0]}*x^2+{p[1]}*x+{p[2]}'
    if deg == 3:
        return [p[0]*x**3+p[1]*x**2+p[2]*x+p[3] for x in x], "Полином 3 степени" #f'{p[0]}*x^3+{p[1]}*x^2+{p[2]}*x+{p[3]}'


def calculate_linear_approximation(x, y):
    p = np.polyfit(x, y, 1)
    x0 = -p[1]/p[0]
    x_list = [x0, x[-1]]
    y_list = [0, p[0]*x[-1]+p[1]]
    return x_list, y_list


def group_by_material(trials):
    grouped_trials = []
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
                                 abrasive_consumption=q.air_consumption,
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
                                                abrasive_consumption=q.air_consumption,
                                                abrasive_type=q.abrasive_type,
                                                nozzle_diam=q.nozzle_diam,
                                                distance_sub=q.distance_sub)
        grouped_trials.append(filtered)
    trials = trials.exclude(id__in=disk_plast_modif_trials)
    return grouped_trials
