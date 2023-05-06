"""
serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipes"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']

    # _ means private or internal method, dont call it outside the code
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Hangle getting or creating ingredient as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)


    def create(self, validated_data):
        """Create a recipe"""
        tag_s = validated_data.pop('tags', [])
        ingredient_s = validated_data.pop('ingredients',[])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tag_s, recipe)
        self._get_or_create_ingredients(ingredient_s, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tag_s = validated_data.pop('tags', None)
        ingredient_s = validated_data.pop('ingredients', None)
        if tag_s is not None:
            instance.tags.clear()
            self._get_or_create_tags(tag_s, instance)
        if ingredient_s is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredient_s, instance)

        for attr, value in validated_data.items():
            setattr(instance,attr, value)

        instance.save()
        return instance




# working with excisting serializers fields so that no code duplicate
class RecipeDetailSerializer(RecipeSerializer):
    """serializer for details recipes view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


