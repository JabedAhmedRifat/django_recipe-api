"""
serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipes"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']

# working with excisting serializers fields so that no code duplicate
class RecipeDetailSerializer(RecipeSerializer):
    """serializer for details recipes view."""

    class Meta(RecipeSerializer.Meta):
        field = RecipeSerializer.Meta.fields + ['description']
