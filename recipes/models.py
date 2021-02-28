from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()
TAGS = ('breakfast', 'lunch', 'dinner')


class TagManager(models.Manager):
    def get_request_tags(self, request):
        tag_set = []
        for tag in TAGS:
            if request.GET.get(tag) == 'on' or request.GET.get(tag) is None:
                obj = self.get(name=tag)
                tag_set.append(obj)
        return tag_set

    def get_recipe_tags(self, request):
        tag_set = []
        for tag in TAGS:
            try:
                request.POST[tag]
                obj, created = self.get_or_create(name=tag)
                tag_set.append(obj)
            except KeyError:
                pass
        return tag_set


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=False, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other


class BasicIngredient(models.Model):
    name = models.CharField(max_length=300)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1),]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(
        BasicIngredient,
        through='RecipeIngredient',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    quantity = models.PositiveSmallIntegerField()
    ingredient = models.ForeignKey(
        BasicIngredient,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    @classmethod
    def create_ingredient(cls, quantity, ingredient, recipe):
        cls.objects.create(quantity=quantity, ingredient=ingredient, recipe=recipe)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchases')
