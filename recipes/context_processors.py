from django.conf import settings


def tag_processor(request):
    return {'TAGS': settings.TAGS}
