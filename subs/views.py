from collections import defaultdict
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from recipes.models import Recipe, RecipeIngredient
from recipes.views import get_request_tags


User = get_user_model()


@login_required
def subscription_list(request):
    followed_authors = User.objects.filter(following__user=request.user)
    paginator = Paginator(followed_authors, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'myFollow.html', {
            'page': page,
            'paginator': paginator,
            }
        )


@login_required
def favorite_list(request):
    user = request.user
    tags = get_request_tags(request)
    all_recipes = Recipe.objects.filter(favorites__user=user)
    purchase_recipes = Recipe.objects.filter(purchases__user=user)
    recipe_list = Recipe.objects.filter(
        id__in=all_recipes, tags__in=tags
    ).distinct()
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html', {
            'user': user,
            'page': page,
            'paginator': paginator,
            'favorite_recipes': all_recipes,
            'purchase_recipes': purchase_recipes,
            }
        )


@login_required
def shop_list(request):
    user = request.user
    recipe_list = Recipe.objects.filter(purchases__user=user)
    return render(
        request,
        'shopList.html', {
            'recipe_list': recipe_list,
            }
        )


@login_required
def get_purchases(request):
    user = request.user
    all_recipes = Recipe.objects.filter(purchases__user=user)
    rlist = RecipeIngredient.objects.filter(
        recipe__in=all_recipes,
    )
    shopping_items = defaultdict(int)
    for item in rlist:
        item_name = f'{item.ingredient.name} ({item.ingredient.unit})'
        shopping_items[item_name] += item.quantity

    file_data = '\n'.join(f'{k} - {v}' for k, v in shopping_items.items())
    response = HttpResponse(file_data,
                            content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
    return response
