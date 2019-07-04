# cooking/serializers.py

from rest_framework import serializers
from .models import FoodCategory
from .models import Recipe
from .models import Ingredient
from .models import RecipeIngredient
from .models import Procedure

class FoodCategorySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = FoodCategory
        fields = ('id', 'name')
    
class RecipeSerializer(serializers.ModelSerializer):
    # food category of the recipe
    foodcategory_name = serializers.CharField(source='foodcategory.name', read_only=True)
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'foodcategory',
            'foodcategory_name',
            'prep_time_from',
            'prep_time_to',
            'cooking_time_from',
            'cooking_time_to',
            'description',
            'image_path'
            )

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe', 'ingredient', 'ingredient_name', 'quantity', 'details', 'order')

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ('id', 'recipe', 'description', 'order')