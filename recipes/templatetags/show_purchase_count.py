from django import template

register = template.Library()

@register.simple_tag
def show_purchase_count(count):
    if count > 0:
        return count
    return ''
