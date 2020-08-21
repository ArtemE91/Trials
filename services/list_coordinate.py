from Sample.models import Sample
from Trial.models import Trials
import numpy as np


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
            trial_group_info['trend_lines'] = get_trend_traces(trial_group_info['traces'])
            trials_info.append(trial_group_info)
    all_traces = []
    trend_ids = []
    for ti in trials_info:
        all_traces += ti['traces']
        trend_ids.append(list(range(len(all_traces), len(all_traces)+len(ti['trend_lines']))))
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
        'mode': 'markers',
    }
    return trace


def get_trend_traces(traces):
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
            'text': function_equation
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
    x0 = -p[1]/p[0]
    x_list = [x0, x[-1]]
    y_list = [0, p[0]*x[-1]+p[1]]
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
