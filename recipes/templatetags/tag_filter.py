import copy

from django import template

from recipes.models import Tag

register = template.Library()


@register.simple_tag
def query_transform(request, item, status):
    updated = request.GET.copy()
    updated[item] = status
    return updated.urlencode()


@register.simple_tag
def get_tags(request):
    tag_list = Tag.get_params()
    tags = copy.deepcopy(tag_list)
    for tag in tags:
        if request.GET.get(tag) == 'off':
            tags[tag]['status'] = 'off'
            tags[tag]['path'] = query_transform(request, item=tag, status='on')
        else:
            tags[tag]['status'] = 'on'
            tags[tag]['path'] = query_transform(request, item=tag, status='off')
    return tags


@register.simple_tag
def get_recipe_tags(recipe_tags):
    tag_list = Tag.get_params()
    tags = copy.deepcopy(tag_list)
    for recipe_tag in recipe_tags:
        tags[recipe_tag.name]['status'] = 'on'
    return tags
