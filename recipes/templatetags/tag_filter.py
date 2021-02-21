from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()


@register.simple_tag
def get_tags(request):
    TAGS = {
        'breakfast': {
            'name': 'Завтрак',
            'style': 'tags__checkbox_style_orange',
            'badge': 'badge_style_orange',
            'status': 'on',
            'path': ''
        },
        'lunch': {
            'name': 'Обед',
            'style': 'tags__checkbox_style_green',
            'badge': 'badge_style_green',
            'status': 'on',
            'path': ''
        },
        'dinner': {
            'name': 'Ужин',
            'style': 'tags__checkbox_style_purple',
            'badge': 'badge_style_purple',
            'status': 'on',
            'path': ''
        }
    }

    for tag in TAGS.keys():
        if request.GET.get(tag) == 'off':
            TAGS[tag]['status'] = 'off'
            kw = {tag: 'on'}
            TAGS[tag]['path'] = query_transform(request, **kw)
        else:
            TAGS[tag]['status'] = 'on'
            kw = {tag: 'off'}
            TAGS[tag]['path'] = query_transform(request, **kw)
    return TAGS

@register.simple_tag
def get_recipe_tags(recipe_tags):
    TAGS = {
        'breakfast': {
            'name': 'Завтрак',
            'badge': 'badge_style_orange',
            'status': 'off',
        },
        'lunch': {
            'name': 'Обед',
            'badge': 'badge_style_green',
            'status': 'off',
        },
        'dinner': {
            'name': 'Ужин',
            'badge': 'badge_style_purple',
            'status': 'off',
        }
    }

    for recipe_tag in recipe_tags:
        TAGS[recipe_tag.name]['status'] = 'on'
    return TAGS
