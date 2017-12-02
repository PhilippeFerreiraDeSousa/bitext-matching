from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(Category, related_name='ingredients')  # enable to call ingredients: [IngredientType] as a field of category

    def __str__(self):
        return self.name

class Link(models.Model):
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
