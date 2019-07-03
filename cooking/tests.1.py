# cooking/tests.py

from django.test import TestCase
from .models import FoodCategory
from .models import Recipe
from .models import Ingredient
from .models import RecipeIngredient
from .models import RecipeProcedure

from .serializers import FoodCategorySerializer
from .serializers import RecipeSerializer
from .serializers import IngredientSerializer
from .serializers import RecipeIngredientSerializer

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class FoodCategoryTestCase(TestCase):
    """ Test Case for Food Category """
    def setUp(self):
        self.client = APIClient()
        self.test = FoodCategory.objects.create(name='Test')
        self.test1 = FoodCategory.objects.create(name='Test1')
        self.test2 = FoodCategory.objects.create(name='Test2')
        self.test3 = FoodCategory.objects.create(name='Test3')

    def test_api_can_get_all_food_category(self):
        # Try to get all food categories from api
        response = self.client.get(reverse('foodcategory'))
        # Actual get of all food categories
        foodcategories = FoodCategory.objects.all()
        serializer = FoodCategorySerializer(foodcategories, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_create_a_food_category(self):
        foodcategory_data = {'name': 'Hors'}
        response = self.client.post(
            reverse('foodcategory'),
            foodcategory_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_valid_food_category(self):
        """ GET A VALID SINGLE FOOD CATEGORY """

        response = self.client.get(
            reverse('foodcategory_details', kwargs={'pk': self.test2.id}),
            format='json')
        foodcategory = FoodCategory.objects.get(pk=self.test2.id)
        serializer = FoodCategorySerializer(foodcategory)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, foodcategory)

    def test_api_can_get_an_invalid_food_category(self):
        """ GET AN INVALID SINGLE FOOD CATEGORY """
        response = self.client.get(
            reverse('foodcategory_details', kwargs={'pk': 10000}),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_can_update_a_food_category(self):
        """ UPDATE A SINGLE FOOD CATEGORY """
        change_foodcategory = {'name': 'xxx'}
        response = self.client.put(
            reverse('foodcategory_details', kwargs={'pk': self.test1.id}),
            change_foodcategory,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_food_category(self):
        """ CAN DELETE A FOOD CATEGORY """
        response = self.client.delete(
            reverse('foodcategory_details', kwargs={'pk': self.test.id}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class RecipeTestCase(TestCase):
    """
        This class defines the test case for creating a whole recipe
    """
    def setUp(self):
        self.client = APIClient()
        # FOOD CATEGORY
        self.foodcategory = FoodCategory.objects.create(name='Main Course')
        # INGREDIENTS
        self.salt = Ingredient.objects.create(name='Salt')
        self.pepper = Ingredient.objects.create(name='pepper')
        self.steak = Ingredient.objects.create(name='steak')
        # RECIPE
        self.recipe = Recipe.objects.create(
            name='Steak',
            foodcategory_id=self.foodcategory.id
        )
        # Procedures
        self.procedure1 = RecipeProcedure.objects.create(
            recipe_id=self.recipe.id,
            order=1,
            description="Cover Steak with salt and pepper")
        self.procedure2 = RecipeProcedure.objects.create(
            recipe_id=self.recipe.id,
            order=2,
            description="Heat Pan for high")
        self.procedure3 = RecipeProcedure.objects.create(
            recipe_id=self.recipe.id,
            order=3,
            description="Cook each side for at 3min (Medium Rare)")
        # RecipeIngredients
        self.recipeIngredient1 = RecipeIngredient.objects.create(
            recipe_id=self.recipe.id,
            quantity="2 Tablespoons",
            description="Test",
            order=1,
            ingredient_id=self.salt.id
        )
        self.recipeIngredient2 = RecipeIngredient.objects.create(
            recipe_id=self.recipe.id,
            quantity="2 Tablespoons",
            description="Test",
            order=2,
            ingredient_id=self.pepper.id
        )
        self.recipeIngredient3 = RecipeIngredient.objects.create(
            recipe_id=self.recipe.id,
            quantity="2 Tablespoons",
            description="Test",
            order=3,
            ingredient_id=self.steak.id
        )

    def test_cooking_can_get_all_recipes(self):
        response = self.client.get(reverse('recipe'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_cooking_can_get_an_invalid_recipe():
    #     pass
    
    def test_cooking_can_get_a_valid_recipe(self):
        """
            [GET] gets a recipe along with its ingredients and procedures
        """
        response = self.client.get(
            reverse('recipe_details', kwargs={'pk': self.recipe.id}),
            format='json'
        )
        # recipe = Recipe.objects.get(pk=self.recipe.id)
        # recipe_ingredients = RecipeIngredient.objects.filter(recipe_id=self.recipe.id)
        #
        # recipe_serializer = RecipeSerializer(recipe)
        # recipe_ingredients_serializer = RecipeIngredientSerializer(recipe_ingredients)

        # self.assertContains(response, recipe_serializer.data)
        # self.assertContains(response, recipe_ingredients_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cooking_can_create_a_recipe(self):
        """ test case to create a whole recipe with procedure and ingredients """

        recipe_data = {
            'name': 'Medium Rare Steak',
            'foodcategory': self.foodcategory.id,
            'ingredients': [
                {
                    'ingredient': self.salt.id,
                    'description': 'Salt',
                    'quantity': '2 Tablespoons',
                    'order': 1
                },
                {
                    'ingredient': self.pepper.id,
                    'description': 'Salt',
                    'quantity': '2 Tablespoons',
                    'order': 2
                },
                {
                    'ingredient': self.steak.id,
                    'description': 'Salt',
                    'quantity': '1 Thick Cut',
                    'order': 3
                }
            ],
            'procedures': [
                'Cover Steak with salt and pepper (Cumin Optional)',
                'Cook each side in a searing hot pan for 3 min',
                'Rest for 6 minutes'
            ]
        }
        response = self.client.post(
            reverse('recipe'),
            recipe_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_delete_recipe(self):
        """ This class defines the test case to delete a recipe """

        response = self.client.delete(
            reverse('recipe_details', kwargs={'pk': self.recipe.id}),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class IngredientTestCase(TestCase):
    """
        This class defines the test case for views in ingredient
    """
    def setUp(self):
        self.client = APIClient()
        self.ingredient1 = Ingredient.objects.create(name='Ingredient1')

    def test_cooking_can_get_all_ingredient(self):
        """ Get all Ingredient """
        response = self.client.get(reverse('ingredient'))

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cooking_can_create_an_ingredient(self):
        """ Creating an Ingredient """
        ingredient_data = {'name': 'Ingredient'}
        response = self.client.post(
            reverse('ingredient'),
            ingredient_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cooking_can_get_valid_ingredient(self):
        response = self.client.get(
            reverse('ingredient_details', kwargs={'pk': self.ingredient1.id}),
            format='json'
        )
        ingredient = Ingredient.objects.get(pk=self.ingredient1.id)
        serializer = IngredientSerializer(ingredient)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cooking_can_get_invalid_ingredient(self):
        response = self.client.get(
            reverse('ingredient_details', kwargs={'pk': 2311}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateWholeRecipeTestCase(TestCase):
    """ This class defines the test case for the models in making a recipe """

    def setUp(self):
        self.foodcategory = FoodCategory(name='Main Course')
        self.foodcategory_old_count = FoodCategory.objects.count()
        self.foodcategory.save()
        # Ingredients
        self.salt = Ingredient(name='Salt')
        self.pepper = Ingredient(name='Pepper')
        self.steak = Ingredient(name='Steak')
        self.ingredient_old_count = Ingredient.objects.count()
        self.salt.save()
        self.pepper.save()
        self.steak.save()
        # Recipe
        self.recipe = Recipe(
            name='Steak',
            foodcategory=self.foodcategory
        )
        self.recipe_old_count = Recipe.objects.count()
        self.recipe.save()
        # Procedures
        self.procedure1 = RecipeProcedure(
            recipe=self.recipe,
            order=1,
            description="Cover Steak with salt and pepper")
        self.procedure2 = RecipeProcedure(
            recipe=self.recipe,
            order=2,
            description="Heat Pan for high")
        self.procedure3 = RecipeProcedure(
            recipe=self.recipe,
            order=3,
            description="Cook each side for at 3min (Medium Rare)")
        # RecipeIngredients
        self.recipeIngredient1 = RecipeIngredient(
            recipe=self.recipe,
            order=1,
            ingredient=self.salt
        )
        self.recipeIngredient2 = RecipeIngredient(
            recipe=self.recipe,
            order=2,
            ingredient=self.pepper
        )
        self.recipeIngredient3 = RecipeIngredient(
            recipe=self.recipe,
            order=3,
            ingredient=self.steak
        )

    def test_model_can_create_a_food_category(self):
        """ Test the FoodCategory model can create a food category """
        new_count = FoodCategory.objects.count()
        self.assertNotEqual(self.foodcategory_old_count, new_count)
    
    def test_model_can_create_an_ingredient(self):
        new_count = Ingredient.objects.count()
        self.assertNotEqual(self.ingredient_old_count, new_count)
    
    def test_model_can_create_a_recipe(self):
        new_count = Recipe.objects.count()
        self.assertNotEqual(self.recipe_old_count, new_count)

    def test_model_can_create_a_procedure(self):
        old_count = RecipeProcedure.objects.count()
        self.procedure1.save()
        self.procedure2.save()
        self.procedure3.save()
        new_count = RecipeProcedure.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_recipeingredient(self):
        old_count = RecipeIngredient.objects.count()
        self.recipeIngredient1.save()
        self.recipeIngredient2.save()
        self.recipeIngredient3.save()
        new_count = RecipeIngredient.objects.count()
        self.assertNotEqual(old_count, new_count)

class SortRecipeTestCase(TestCase):
    """
    Get all recipe by sorted type (1: hors, 2: appetizer ....)
    """
    def setUp(self):
        self.client = APIClient()
        self.foodcategory = FoodCategory.objects.create(name='Hors')
        self.foodcategory2 = FoodCategory.objects.create(name='Appetizer')
        self.foodcategory3 = FoodCategory.objects.create(name='Salad')
        self.foodcategory4 = FoodCategory.objects.create(name='Main Course')
        self.foodcategory5 = FoodCategory.objects.create(name='Dessert')

        self.recipe = Recipe.objects.create(
            name="Test",
            foodcategory_id=self.foodcategory.id
        )
        self.recipe2 = Recipe.objects.create(
            name="TestMian",
            foodcategory_id=self.foodcategory4.id
        )

    def test_cooking_can_get_sorted_recipes(self):
        """ Gets recipes by its foodcategory """

        url = '/cooking/recipe/'
        query_params = {'foodcategory': self.foodcategory.id}
        response = self.client.get(url, query_params)

        # Actual Data
        recipe = Recipe.objects.filter(foodcategory=self.foodcategory.id)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_cooking_can_get_empty_recipe(self):
        """ Checks if can get empty recipes """

        response = self.client.get('/cooking/recipe/', {'foodcategory': 1998})
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cooking_can_get_default_recipes(self):
        """ Get the default recipe, foodcategory_id = 4(Main Course) """

        url = '/cooking/recipe/'
        response = self.client.get(url)
        # Actual Data
        default_recipes = Recipe.objects.filter(pk=4)
        serializer = RecipeSerializer(default_recipes, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

