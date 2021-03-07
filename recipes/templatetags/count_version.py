from django import template

register = template.Library()


@register.simple_tag
def count_version(count):
    if 4 < count % 100 < 21:
        return f'{count} рецептов...'
    elif count % 10 == 1:
        return f'{count} рецепт...'
    elif 1 < count % 10 < 5:
        return f'{count} рецепта...'
    else:
        return f'{count} рецептов...'
