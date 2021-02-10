import csv

from recipes.models import BasicIngredient

with open('ingredients/ingredients.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        obj, created = BasicIngredient.objects.get_or_create(
            name=row[0],
            unit=row[1],
        )
