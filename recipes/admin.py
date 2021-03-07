from django.contrib import admin

from .models import (BasicIngredient, Favorite, Purchase, Recipe,
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
    list_display = ('name', 'display_name', 'style', 'badge')
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.register(BasicIngredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
