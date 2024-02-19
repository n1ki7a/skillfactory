import re

from django import template

register = template.Library()

OBSCENE_WORDS = [
    'редиска',
    'какашка',
    'альбом'
]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError

    return re.sub(r'(' + '|'.join(OBSCENE_WORDS) + ')', replacer, value, flags=re.IGNORECASE)


def replacer(match):
    x = match.group()
    return x[:1] + '*' * (len(x)-1)
