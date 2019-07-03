# cooking/tests.py

from django.test import TestCase

from .models import FoodCategory
from .models import Recipe
from .models import RecipeIngredient
from .models import Procedure
from .models import Ingredient

from .serializers import FoodCategorySerializer
from .serializers import IngredientSerializer
from .serializers import RecipeSerializer
from .serializers import RecipeIngredientSerializer
from .serializers import ProcedureSerializer

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

client = APIClient()

class FoodCategoryTestCase (TestCase):
    """ Test case for food category """
    def setUp(self):
        self.object1 = FoodCategory.objects.create(name='Hors')
        self.object2 = FoodCategory.objects.create(name='Appetizer')
        self.object3 = FoodCategory.objects.create(name='Soup')
        self.object4 = FoodCategory.objects.create(name='Main')
        self.object5 = FoodCategory.objects.create(name='Dessert')
    
    def test_api_can_get_all_food_category(self):
        # Try to get all food category from api (Runs the url function foodcategory)
        response = client.get(reverse('foodcategory'))
        # Get instantly the objects here
        foodcategories = FoodCategory.objects.all()

        serializer = FoodCategorySerializer(foodcategories, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class IngredientTestCase (TestCase):
    def setUp(self):
        self.object1 = Ingredient.objects.create(name='Object1')
        self.object2 = Ingredient.objects.create(name='Object2')
    
    def test_api_can_get_all_ingredient(self):
        # Try to get all ingredient from api (Runs the url function ingredient)
        response = client.get(reverse('ingredient'))
        # Get instantly the objects here
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecipeTestCase (TestCase):

    def setUp(self):
        self.main_course = FoodCategory.objects.create(name='Main')
        self.shoyu = Recipe.objects.create(
            name='Shoyu Ramen',
            foodcategory_id=self.main_course.id,
            prep_time_from='5',
            prep_time_to='15',
            cooking_time_from='30',
            cooking_time_to='60',
            description='Hot noodle soup that is consists of soy based seasoning',
            image_path='ramen.jpg'
            )
        
        # Ingredients
        self.soy = Ingredient.objects.create(name='Soy')
        self.broth = Ingredient.objects.create(name='Broth')
        self.egg = Ingredient.objects.create(name='Egg')

        # Recipe Ingredients

        self.ingredient_1 = RecipeIngredient.objects.create(
            recipe_id=self.shoyu.id,
            ingredient_id=self.soy.id,
            quantity='2tbsp',
            detail='Dark Soy Sauce',
            order=1
        )
        self.ingredient_2 = RecipeIngredient.objects.create(
            recipe_id=self.shoyu.id,
            ingredient_id=self.broth.id,
            quantity='2 Cups',
            detail='',
            order=2
        )
        self.ingredient_3 = RecipeIngredient.objects.create(
            recipe_id=self.shoyu.id,
            ingredient_id=self.egg.id,
            quantity='1',
            detail='Soft Boiled',
            order=3
        )

        # Procedures
        self.step_1 = Procedure.objects.create(
            recipe_id=self.shoyu.id,
            description='Cook Broth',
            order=1)
        self.step_2 = Procedure.objects.create(
            recipe_id=self.shoyu.id,
            description='Cook Egg',
            order=2)
        self.step_3 = Procedure.objects.create(
            recipe_id=self.shoyu.id,
            description='Create Layers, add soy first, then broth, topped with egg',
            order=3)

    def test_api_can_get_ingredients_and_procedures_from_a_recipe(self):
        response = client.get(
            reverse('recipe_details', kwargs={'pk': self.shoyu.id})
        )

        # get recipe
        recipe = Recipe.objects.get(pk=self.shoyu.id)
        recipe_serialized = RecipeSerializer(recipe)

        # get ingredients
        ingredients = RecipeIngredient.objects.get(recipe=self.shoyu.id)
        ingredients_serialized = RecipeIngredientSerializer(ingredients, many=True)

        # get procedures
        procedures = Procedure.objects.get(recipe=self.shoyu.id)
        procedures_serialized = ProcedureSerializer(procedures, many=True)

        self.assertEqual(response.data.recipe, recipe_serialized.data)
        self.assertEqual(response.data.ingredients, ingredients_serialized.data)
        self.assertEqual(response.data.procedures, procedures_serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RecipeByFoodCategoryTestCase (TestCase):
    def setUp(self):
        self.main = FoodCategory.objects.create(name='Main')
        self.appetizer = FoodCategory.objects.create(name='appetizer')

        self.shoyu = Recipe.objects.create(
            name='Shoyu Ramen',
            foodcategory_id=self.main.id,
            prep_time_from='5',
            prep_time_to='15',
            cooking_time_from='30',
            cooking_time_to='60',
            description='Hot noodle soup that is consists of soy based seasoning',
            image_path='ramen.jpg'
            )
        self.steak = Recipe.objects.create(
            name='Pipz Steak',
            foodcategory_id=self.main.id,
            prep_time_from='2',
            prep_time_to='10',
            cooking_time_from='6',
            cooking_time_to='10',
            description='Medium rare steak with chimuchuri dipping sauce',
            image_path='steak.jpg'
            )
        self.invalid_recipe = Recipe.objects.create(
            name='Dumplings',
            foodcategory_id=self.appetizer.id,
            prep_time_from='5',
            prep_time_to='10',
            cooking_time_from='8',
            cooking_time_to='10',
            description='Potstickers filled with pork and vegetable combinationed, crisp on one side and soft on the other',
            image_path='dumplings.jpg'
            )
    
    def test_api_can_get_all_recipe_from_main_course(self):
        response = client.get(
            reverse(
                'recipe',
                kwargs={'foodcategory_id': self.main.id}),
            format='json')
        
        recipes = Recipe.objects.get(foodcategory=self.main.id)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, recipes.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    