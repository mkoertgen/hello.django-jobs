# cf.: https://www.imzjy.com/blog/2018-05-20-render-the-markdown-in-django
from django import template
from django.template.defaultfilters import stringfilter

from markdown import Markdown
MARKDOWN = Markdown(extensions=['markdown.extensions.fenced_code'])

register = template.Library()

@register.filter()
@stringfilter
def markdown(content):
  return MARKDOWN.convert(content)
