from django import template
from slugify import slugify as py_slugify

register = template.Library()

@register.filter
def slugify(value):
    return py_slugify(value)