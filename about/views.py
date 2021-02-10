from django.views.generic.base import TemplateView


class AuthorFlatPage(TemplateView):
    template_name = 'flatpages/author.html'


class TechFlatPage(TemplateView):
    template_name = 'flatpages/tech.html'
