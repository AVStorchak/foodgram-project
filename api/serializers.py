from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import BasicIngredient
from subs.models import Favorite, Purchase, Subscription

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'unit')
        model = BasicIngredient


class SubscriptionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        read_only_fields = ('user',)
        unique_together = ('author', 'user')


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        read_only_fields = ('user',)
        unique_together = ('recipe', 'user')


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Purchase
        fields = ('recipe', 'user')
        read_only_fields = ('user',)
        unique_together = ('recipe', 'user')
