from collections import defaultdict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from api.models import Subscription

from .forms import RecipeForm
from .models import Favorite, Purchase, Recipe, RecipeIngredient, Tag

User = get_user_model()


def handle_ingredients(request, recipe):
    ingredient_names, ingredient_values = {}, {}
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for k, v in request.POST.items():
        if k.startswith('nameIngredient'):
            ingredient_names[k[15:]] = v
        elif k.startswith('valueIngredient'):
            ingredient_values[k[16:]] = v
        else:
            continue
    if len(ingredient_names) != len(ingredient_values):
        return HttpResponseBadRequest('The ingredient data is not valid!')
    for k, ingredient_name in ingredient_names.items():
        quantity = ingredient_values[k]
        RecipeIngredient.create_ingredient(
            quantity=quantity,
            ingredient_name=ingredient_name,
            recipe=recipe
        )


def get_request_tags(request):
    tag_set = []
    tag_list = Tag.get_params()
    for tag, params in tag_list.items():
        if request.GET.get(tag) == 'on' or request.GET.get(tag) is None:
            tag_set.append(params['instance'])
    return tag_set


def get_recipe_tags(request):
    tag_set = []
    tag_list = Tag.get_params()
    for tag, params in tag_list.items():
        if tag in request.POST:
            tag_set.append(params['instance'])
    return tag_set


@cache_page(1)
def index(request):
    tags = get_request_tags(request)
    recipe_list = Recipe.objects.filter(tags__in=tags).distinct()
    favorite_recipes, purchase_recipes = [], []
    if request.user.is_authenticated:
        favorite_recipes = Recipe.objects.filter(favorites__user=request.user)
        purchase_recipes = Recipe.objects.filter(purchases__user=request.user)
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html', {
            'page': page,
            'paginator': paginator,
            'favorite_recipes': favorite_recipes,
            'purchase_recipes': purchase_recipes,
        }
    )


@login_required
def new_recipe(request):
    db_error = None
    tag_error = None
    ingredient_error = None
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        try:
            tags = get_recipe_tags(request)
            if not tags:
                tag_error = 'Вы не можете создать рецепт без тегов'
                return render(
                    request,
                    'formRecipe.html', {
                        'form': form,
                        'db_error': db_error,
                        'tag_error': tag_error,
                        'ingredient_error': ingredient_error
                    }
                )
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            handle_ingredients(request, recipe)
            if len(RecipeIngredient.objects.filter(recipe=recipe)) == 0:
                recipe.delete()
                ingredient_error = 'Вы не можете создать рецепт без ингредиентов'
                return render(
                    request,
                    'formRecipe.html', {
                        'form': form,
                        'db_error': db_error,
                        'tag_error': tag_error,
                        'ingredient_error': ingredient_error
                    }
                )
            for tag in tags:
                recipe.tags.add(tag)
            recipe_url = reverse('recipe', args=(recipe.author, recipe.id))
            return redirect(recipe_url)
        except IntegrityError:
            db_error = 'Вы не можете создавать рецепты с одинаковыми названиями'

    return render(
        request,
        'formRecipe.html', {
            'form': form,
            'db_error': db_error,
            'tag_error': tag_error,
            'ingredient_error': ingredient_error
        }
    )


@login_required
def recipe_edit(request, username, recipe_id):
    db_error = None
    tag_error = None
    ingredient_error = None
    recipe = get_object_or_404(
        Recipe, id=recipe_id, author__username=username
    )
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    tags = recipe.tags.all()

    if recipe.author != request.user:
        recipe_url = reverse('recipe', args=(recipe.author, recipe.id))
        return redirect(recipe_url)

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    if form.is_valid():
        try:
            tags = get_recipe_tags(request)
            if not tags:
                tag_error = 'Вы не можете создать рецепт без тегов'
                return render(
                    request,
                    'formRecipe.html', {
                        'form': form,
                        'recipe': recipe,
                        'ingredients': ingredients,
                        'tags': tags,
                        'db_error': db_error,
                        'tag_error': tag_error,
                        'ingredient_error': ingredient_error
                    }
                )
            handle_ingredients(request, recipe)
            if len(RecipeIngredient.objects.filter(recipe=recipe)) == 0:
                ingredient_error = 'Вы не можете создать рецепт без ингредиентов'
                return render(
                    request,
                    'formRecipe.html', {
                        'form': form,
                        'recipe': recipe,
                        'ingredients': ingredients,
                        'tags': tags,
                        'db_error': db_error,
                        'tag_error': tag_error,
                        'ingredient_error': ingredient_error
                    }
                )
            form.save()
            recipe.tags.clear()
            for tag in tags:
                recipe.tags.add(tag)
            recipe_url = reverse('recipe', args=(recipe.author, recipe.id))
            return redirect(recipe_url)

        except IntegrityError:
            db_error = 'Вы не можете создавать рецепты с одинаковыми названиями'

    return render(
        request,
        'formChangeRecipe.html', {
            'form': form,
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags,
            'db_error': db_error,
            'tag_error': tag_error,
            'ingredient_error': ingredient_error
        }
    )


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(
        Recipe, id=recipe_id, author__username=username
    )

    if recipe.author != request.user:
        recipe_url = reverse('recipe', args=(recipe.author, recipe.id))
        return redirect(recipe_url)

    recipe.delete()

    return redirect('index')


def recipe_view(request, username, recipe_id):
    user = request.user
    recipe = get_object_or_404(
        Recipe.objects, id=recipe_id, author__username=username
    )
    author = recipe.author
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    following = False
    if request.user.is_authenticated:
        following = Subscription.objects.filter(
            author=author, user=user
        ).exists()
        user.is_favorite_recipe = Favorite.objects.filter(
            recipe=recipe, user=user
        ).exists()
        user.is_purchase_recipe = Purchase.objects.filter(
            recipe=recipe, user=user
        ).exists()
    return render(
        request,
        'singlePage.html', {
            'user': user,
            'author': author,
            'recipe': recipe,
            'ingredients': ingredients,
            'following': following,
        }
    )


def profile(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    tags = get_request_tags(request)
    recipe_list = author.recipes.all().filter(tags__in=tags).distinct()
    favorite_recipes, purchase_recipes = [], []
    following = False
    if request.user.is_authenticated:
        favorite_recipes = Recipe.objects.filter(favorites__user=request.user)
        purchase_recipes = Recipe.objects.filter(purchases__user=request.user)
        following = Subscription.objects.filter(
            author=author, user=user
        ).exists()
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'authorRecipe.html', {
            'user': user,
            'author': author,
            'page': page,
            'paginator': paginator,
            'following': following,
            'favorite_recipes': favorite_recipes,
            'purchase_recipes': purchase_recipes,
        }
    )


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


def page_not_found(request, exception):
    return render(
        request,
        'errors/404_error.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        'errors/500_error.html',
        status=500
    )
