from django import template

register = template.Library()


@register.filter()
def censor(value):
    return f'{value} Р'
