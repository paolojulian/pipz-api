# cooking/views.py

from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response
from rest_framework.views import APIView

from .models import FoodCategory
from .models import Recipe
from .models import Ingredient
from .models import RecipeIngredient
from .models import Procedure

from .serializers import FoodCategorySerializer
from .serializers import RecipeSerializer
from .serializers import IngredientSerializer
from .serializers import RecipeIngredientSerializer
from .serializers import ProcedureSerializer

class FoodCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    """ This class handles GET, PUT, and DELETE requests for food category """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

#cooking/recipe
class CreateRecipe(APIView):
    '''
    [POST, GET] This class is used to create a recipe and get recipes by foodcategory
    '''

    def get(self, request):
        foodcategory = request.query_params.get('foodcategory')

        # Set the default value if foodcategory is null
        if not foodcategory:
            foodcategory = 4 # Main Course

        recipes = Recipe.objects.filter(foodcategory=foodcategory)
        serializer = RecipeSerializer(recipes, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            recipe = {
                'name': request.data['name'],
                'foodcategory': request.data['foodcategory']
            }
            recipe_serializer = RecipeSerializer(data=recipe)
            if not recipe_serializer.is_valid():
                return Response(data=recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            recipe = recipe_serializer.save()
            self.recipe_id = RecipeSerializer(recipe).data['id']
            self.save_ingredients(request.data['ingredients'])
            self.save_procedures(request.data['procedures'])

            return Response(data=recipe.response_created(), status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def save_ingredients(self, ingredients):
        ''' Save ingredients of the recipe '''
        for ingredient in ingredients:
            ingredient['recipe'] = self.recipe_id
            ingredient_serializer = RecipeIngredientSerializer(data=ingredient)
            if not ingredient_serializer.is_valid():
                raise Exception(ingredient_serializer.errors)
            ingredient_serializer.save()

    def save_procedures(self, procedures):
        ''' Save procedures of the recipe '''
        for index, description in enumerate(procedures):
            procedure = {
                'recipe': self.recipe_id,
                'description': description,
                'order': index+1
            }
            procedure_serializer = ProcedureSerializer(data=procedure)
            if not procedure_serializer.is_valid():
                raise Exception(procedure_serializer.errors)

            procedure_serializer.save()

#cooking/recipe/{pk}
class RecipeDetails(APIView):
    '''
    [RETRIEVE, UPDATE, DELETE] recipe
    '''

    def get_object(self, pk):
        return Recipe.objects.get(pk=pk)

    def get(self, request, pk):
        ''' Get the whole recipe, (Includes ingredients and procedures) '''

        # Get the recipe, its ingredients and procedures
        recipe = self.get_object(pk)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=pk)
        recipe_procedures = Procedure.objects.filter(recipe=pk)

        # Serialize datas
        recipe_serializer = RecipeSerializer(recipe)
        recipe_ingredients_serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        recipe_procedures_serializer = ProcedureSerializer(recipe_procedures, many=True)

        data = {
            'recipe': recipe_serializer.data,
            'ingredients': recipe_ingredients_serializer.data,
            'procedures': recipe_procedures_serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        # Ingredients and Procedures will be automatically cascaded
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateFoodCategory(generics.ListCreateAPIView):
    """ This class is used to create a food category """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

    def perform_create(self, serializer):
        """save the post data when creating a foodcategory"""
        serializer.save()

class CreateIngredient(generics.ListCreateAPIView):
    ''' [POST, GET] This class is used to create recipes and get all recipes '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """ save the post data when creating an ingredient """
        serializer.save()
    
class IngredientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
