from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import BasicIngredient, Favorite, Purchase, Subscription

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

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        read_only_fields = ('user',)


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        read_only_fields = ('user',)


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = Purchase
        fields = ('recipe', 'user')
        read_only_fields = ('user',)
