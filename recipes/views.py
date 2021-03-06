from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from subs.models import Favorite, Purchase, Subscription
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag


User = get_user_model()


def handle_ingredients(request, recipe):
    ingredient_names, ingredient_values = {}, {}
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for _, v in request.POST.items():
        if 'nameIngredient' in _:
            ingredient_names[_[15:]] = v
        elif 'valueIngredient_' in _:
            ingredient_values[_[16:]] = v
        else:
            continue
    for k, ingredient_name in ingredient_names.items():
        quantity = ingredient_values[k]
        RecipeIngredient.create_ingredient(quantity=quantity,
                                           ingredient_name=ingredient_name,
                                           recipe=recipe)


def get_request_tags(request):
    tag_set = []
    for tag in settings.TAGS:
        if request.GET.get(tag) == 'on' or request.GET.get(tag) is None:
            obj = get_object_or_404(Tag, name=tag)
            tag_set.append(obj)
    return tag_set


def get_recipe_tags(request):
    tag_set = []
    for tag in settings.TAGS:
        if tag in request.POST:
            obj = get_object_or_404(Tag, name=tag)
            tag_set.append(obj)
        else:
            continue
    return tag_set


@cache_page(1)
def index(request):
    tags = get_request_tags(request)
    recipe_list = Recipe.objects.filter(tags__in=tags).distinct()
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
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            tags = get_recipe_tags(request)
            if not tags:
                return render(request, "errors/no_tag_error.html")
            for tag in tags:
                recipe.tags.add(tag)
            handle_ingredients(request, recipe)
            return redirect('index')

    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id=recipe_id, author__username=username)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    tags = recipe.tags.all()
    recipe_url = reverse('recipe', args=(recipe.author, recipe.id))

    if recipe.author != request.user:
        return redirect(recipe_url)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        recipe.tags.clear()
        tags = get_recipe_tags(request)
        for tag in tags:
            recipe.tags.add(tag)
        handle_ingredients(request, recipe)
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
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id=recipe_id, author__username=username)
    recipe_url = reverse('recipe', args=(recipe.author, recipe.id))

    if recipe.author != request.user:
        return redirect(recipe_url)

    recipe.delete()

    return redirect('index')


def recipe_view(request, username, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe.objects,
                               id=recipe_id, author__username=username)
    author = recipe.author
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    following = Subscription.objects.filter(author=author, user=user).exists()
    favorite_recipe = Favorite.objects.filter(recipe=recipe, user=user).exists()
    purchase_recipe = Purchase.objects.filter(recipe=recipe, user=user).exists()
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
    tags = get_request_tags(request)
    recipe_list = author.recipes.all().filter(tags__in=tags).distinct()
    favorite_recipes = Recipe.objects.filter(favorites__user=request.user)
    purchase_recipes = Recipe.objects.filter(purchases__user=request.user)
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
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
