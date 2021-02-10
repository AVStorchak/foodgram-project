from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .forms import RecipeForm
from .models import (BasicIngredient, Favorite, Purchase, Recipe,
                     RecipeIngredient, Subscription, Tag)

User = get_user_model()

@cache_page(1)
def index(request):
    tags = Tag.objects.get_request_tags(request)
    recipe_list = Recipe.objects.filter(tags__in=tags).distinct()
    try:
        favorite_recipes = [i.recipe.id for i in
                            Favorite.objects.filter(user=request.user)]
        purchase_recipes = [i.recipe.id for i in
                            Purchase.objects.filter(user=request.user)]
    except TypeError:
        favorite_recipes, purchase_recipes = [], []
    paginator = Paginator(recipe_list, 6)
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
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            tags = Tag.objects.get_recipe_tags(request)
            if tags == []:
                return render(request, "errors/no_tag_error.html")
            recipe.apply_tags(tags)
            RecipeIngredient.objects.handle_ingredients(request, recipe, BasicIngredient)
            return redirect('index')

    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, username, post_id):
    recipe = get_object_or_404(Recipe.objects.select_related('author'),
                               id=post_id, author__username=username)
    ingredients = [i for i in RecipeIngredient.objects.filter(recipe=recipe)]
    tags = recipe.tags.all
    recipe_url = reverse('recipe', args=(recipe.author, recipe.id))

    if recipe.author != request.user:
        return redirect(recipe_url)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        recipe.tags.clear()
        tags = Tag.objects.get_recipe_tags(request)
        recipe.apply_tags(tags)
        RecipeIngredient.objects.handle_ingredients(request, recipe, BasicIngredient)
        return redirect(recipe_url)

    return render(
        request,
        'formChangeRecipe.html', {
            'form': form,
            'recipe': recipe,
            'ingredients': ingredients,
            'tags': tags
            }
        )


@login_required
def recipe_delete(request, username, post_id):
    recipe = get_object_or_404(Recipe.objects.select_related('author'),
                               id=post_id, author__username=username)
    recipe_url = reverse('recipe', args=(recipe.author, recipe.id))

    if recipe.author != request.user:
        return redirect(recipe_url)

    recipe.delete()

    return redirect('index')


def recipe_view(request, username, post_id):
    user = request.user
    recipe = get_object_or_404(Recipe.objects, id=post_id, author__username=username)
    author = recipe.author
    ingredients = [i for i in RecipeIngredient.objects.filter(recipe=recipe)]
    following = False
    favorite_recipe = False
    purchase_recipe = False
    for item in author.following.all():
        if item.user == user:
            following = True
            break
    for item in recipe.favorites.all():
        if item.user == user:
            favorite_recipe = True
            break
    for item in recipe.purchases.all():
        if item.user == user:
            purchase_recipe = True
            break
    return render(
        request,
        'singlePage.html', {
            'user': user,
            'author': author,
            'recipe': recipe,
            'ingredients': ingredients,
            'following': following,
            'favorite_recipe': favorite_recipe,
            'purchase_recipe': purchase_recipe
            }
        )


def profile(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    tags = Tag.objects.get_request_tags(request)
    recipe_list = author.recipes.all().filter(tags__in=tags).distinct()
    favorite_recipes = [i.recipe.id for i in
                        Favorite.objects.filter(user=user)]
    purchase_recipes = [i.recipe.id for i in
                        Purchase.objects.filter(user=request.user)]
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    for item in author.following.all():
        if item.user == user:
            following = True
            break
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
    followed_authors = [i.author for i in
                        Subscription.objects.filter(user=request.user)]
    paginator = Paginator(followed_authors, 6)
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
    tags = Tag.objects.get_request_tags(request)
    all_recipes = [i.recipe.id for i in
                   Favorite.objects.filter(user=user)]
    recipe_list = Recipe.objects.filter(
        id__in=all_recipes, tags__in=tags
    ).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'favorite.html', {
            'user': user,
            'page': page,
            'paginator': paginator,
            'favorite_recipes': all_recipes,
            }
        )


@login_required
def shop_list(request):
    user = request.user
    all_recipes = [i.recipe.id for i in
                   Purchase.objects.filter(user=user)]
    recipe_list = Recipe.objects.filter(
        id__in=all_recipes,
    ).distinct()
    return render(
        request,
        'shopList.html', {
            'recipe_list': recipe_list,
            }
        )


@login_required
def get_purchases(request):
    user = request.user
    all_recipes = [i.recipe.id for i in
                   Purchase.objects.filter(user=user)]
    rlist = RecipeIngredient.objects.filter(
        recipe__in=all_recipes,
    )
    shopping_items = {}
    for item in rlist:
        item_name = f'{item.ingredient.name} ({item.ingredient.unit})'
        try:
            shopping_items[item_name] += item.quantity
        except KeyError:
            shopping_items[item_name] = item.quantity

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
