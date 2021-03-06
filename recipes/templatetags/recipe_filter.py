from django import template

register = template.Library()


@register.filter
def exists(obj, qset):
    return obj in qset
