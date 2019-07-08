#cooking/urls.py

from django.urls import include, re_path

from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateFoodCategory
from .views import FoodCategoryDetails

from .views import CreateRecipe
from .views import RecipeDetails

from .views import CreateIngredient
from .views import IngredientDetails

urlpatterns = [
    # FOOD CATEGORY
    # POST - create food category, GET - get all food category
    re_path(r'^foodcategory/$', CreateFoodCategory.as_view(), name='foodcategory'),
    # PUT, DELETE, GET
    re_path(r'^foodcategory/(?P<pk>[0-9]+)/$', FoodCategoryDetails.as_view(), name='foodcategory_details'),

    # RECIPE
    # POST - create food category, GET - get all recipes by food category
    re_path(r'^recipe/$', CreateRecipe.as_view(), name='recipe'),
    re_path(r'^recipe/(?P<pk>[0-9]+)/$', RecipeDetails.as_view(), name='recipe_details'),

    # INGREDIENT
    # POST - create ingredient, GET - get all ingredients
    re_path(r'^ingredient/$', CreateIngredient.as_view(), name='ingredient'),
    re_path(r'^ingredient/(?P<pk>[0-9]+)/$', IngredientDetails.as_view(), name='ingredient_details')
]

# urlpatterns = format_suffix_patterns(urlpatterns)
