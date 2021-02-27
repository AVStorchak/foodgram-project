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

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        read_only_fields = ('user',)

    def validate(self, data):
        author = self.context['request'].data['author']
        user = self.context['request'].user
        subscription = Subscription.objects.filter(author__username=author, user=user)
        if len(subscription) != 0 and author == user:
            raise serializers.ValidationError('!!!')
        else:
            return data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        read_only_fields = ('user',)

    def validate(self, data):
        recipe = self.context['request'].data['id']
        user = self.context['request'].user
        favorite = Favorite.objects.filter(recipe=recipe, user=user)
        if len(favorite) != 0:
            raise serializers.ValidationError('!!!')
        else:
            return data


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Purchase
        fields = ('recipe', 'user')
        read_only_fields = ('user',)

    def validate(self, data):
        recipe = self.context['request'].data['id']
        user = self.context['request'].user
        purchase = Purchase.objects.filter(recipe=recipe, user=user)
        if len(purchase) != 0:
            raise serializers.ValidationError('!!!')
        else:
            return data
