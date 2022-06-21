from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def cut(value):
    """Extrait la premiere phrase d'un blog post"""
    dot = value.index('.')

    return mark_safe(value[:(dot + 1)])
