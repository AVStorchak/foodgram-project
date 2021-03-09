from .models import Tag


def tag_processor(request):
    tag_params = Tag.get_params()
    return {'tag_params': tag_params}
