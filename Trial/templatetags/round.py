from django import template

register = template.Library()


@register.filter(name='round_weight')
def round_weight(value):
    return round(value, 5)
