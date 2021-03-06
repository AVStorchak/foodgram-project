import copy
from django import template
from django.conf import settings

from recipes.models import Tag

register = template.Library()


@register.simple_tag
def query_transform(request, item, status):
    updated = request.GET.copy()
    updated[item] = status
    return updated.urlencode()


@register.simple_tag
def get_tags(request):
    tags = copy.deepcopy(settings.TAGS)
    for tag in tags:
        if not Tag.objects.filter(name=tag).exists():
            Tag.objects.create(name=tag)
        if request.GET.get(tag) == 'off':
            tags[tag]['status'] = 'off'
            tags[tag]['path'] = query_transform(request, item=tag, status='on')
        else:
            tags[tag]['status'] = 'on'
            tags[tag]['path'] = query_transform(request, item=tag, status='off')
    return tags


@register.simple_tag
def get_recipe_tags(recipe_tags):
    tags = copy.deepcopy(settings.TAGS)
    for recipe_tag in recipe_tags:
        tags[recipe_tag.name]['status'] = 'on'
    return tags
