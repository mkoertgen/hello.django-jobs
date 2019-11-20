# cf.: https://www.imzjy.com/blog/2018-05-20-render-the-markdown-in-django
from django import template
from django.template.defaultfilters import stringfilter

import humanize

register = template.Library()


@register.filter()
@stringfilter
def naturaldelta(duration):
    return humanize.naturaldelta(duration)
