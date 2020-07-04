from Sample.models import Sample


def get_list_coordinate(sample_ids: list) -> dict:
    samples = Sample.objects.filter(pk__in=sample_ids)
    related_trials = [sample.sample for sample in samples if hasattr(sample, 'sample')]
    coordinates = {}

    for trial in related_trials:
        related_experiments = trial.trials_values.all().order_by('time_trials')
        weight_loss = [round(trial.sample.weight - experiment.change_weight, 5) for experiment in related_experiments]
        times = [experiment.time_trials for experiment in related_experiments]
        coordinates[str(trial.sample)] = {'times': times, 'weight': weight_loss}
    return coordinates
