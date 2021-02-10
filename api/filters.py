import django_filters

from recipes.models import BasicIngredient


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')

    class Meta:
        model = BasicIngredient
        fields = ('id',)
