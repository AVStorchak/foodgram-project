from .models import Tag


def tag_processor(request):
    TAGS = {}
    tag_list = Tag.objects.all()
    for tag in tag_list:
        params = {}
        params['name'] = tag.display_name
        params['style'] = tag.style
        params['badge'] = tag.badge
        params['status'] = ''
        params['path'] = ''
        TAGS[tag.name] = params
    return {'TAGS': TAGS}
