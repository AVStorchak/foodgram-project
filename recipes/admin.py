from django.contrib import admin

from .models import (BasicIngredient, Recipe,
                     RecipeIngredient, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('title', 'author', 'tags')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit',)
    list_filter = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'ingredient', 'recipe')
    search_fields = ('recipe',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(BasicIngredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
