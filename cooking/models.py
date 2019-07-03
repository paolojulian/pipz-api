# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

class FoodCategory(models.Model):
    ''' FOOD CATEGORIES, 1 = Hors, 2 = Appetizers, 3 = Salads, 4 = Main Course, 5 = Dessert '''
    name = models.CharField(max_length=100, blank=False, unique=True)
    def __str__(self):
        ''' returs a human readable representation of the model instance '''
        return "{}".format(self.name)

    def response_created(self):
        return f"{self.name} has been successfully created"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    foodcategory = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    prep_time_from = models.PositiveIntegerField(blank=True, default=0)
    prep_time_to = models.PositiveIntegerField(blank=True, default=5)
    cooking_time_from = models.PositiveIntegerField(blank=True, default=0)
    cooking_time_to = models.PositiveIntegerField(blank=True, default=5)
    description = models.TextField(blank=True)
    image_path = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return "{}".format(self.name)

    def response_created(self):
        return f"{self.name} has been successfully created"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100, default='')
    details = models.TextField(default='')
    order = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=1)

    class Meta:
        unique_together = ['recipe', 'ingredient', 'order']
        unique_together = ['recipe', 'ingredient']
        unique_together = ['recipe', 'order']
        ordering = ['order']

class RecipeProcedure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=1)

    class Meta:
        unique_together = ['recipe', 'order']
        ordering = ['order']

class Procedure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=1)

    class Meta:
        unique_together = ['recipe', 'order']
        ordering = ['order']
