# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Message(models.Model):
    user = models.ForeignKey('auth.User')
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

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

class Bitext(models.Model):
    french = models.TextField(null=True, blank=True)
    english = models.TextField(null=True, blank=True)
