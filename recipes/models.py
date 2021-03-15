from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=False, unique=True)
    display_name = models.CharField(max_length=20, blank=True, unique=True)
    style = models.CharField(max_length=70, blank=True)
    badge = models.CharField(max_length=70, blank=True)

    @classmethod
    def get_params(cls):
        tag_params = {}
        tag_list = cls.objects.all()
        for tag in tag_list:
            params = {}
            params['instance'] = tag
            params['name'] = tag.display_name
            params['style'] = tag.style
            params['badge'] = tag.badge
            params['status'] = ''
            params['path'] = ''
            tag_params[tag.name] = params
        return tag_params

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
        constraints = [
            models.UniqueConstraint(fields=['name', 'unit'], name='ingredient')
        ]


class Recipe(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1), ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(
        BasicIngredient,
        through='RecipeIngredient',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='recipes/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='recipe')
        ]


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
    def create_ingredient(cls, quantity, ingredient_name, recipe):
        ingredient = get_object_or_404(BasicIngredient, name=ingredient_name)
        recipe = get_object_or_404(Recipe, id=recipe.id)
        cls.objects.create(quantity=quantity,
                           ingredient=ingredient,
                           recipe=recipe)


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
