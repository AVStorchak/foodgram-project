from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from recipes.models import BasicIngredient, Favorite, Purchase, Recipe

from .models import Subscription
from .permissions import IsOwnerOrSuperuserOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)

User = get_user_model()


JSON_RESPONSES = {'success': JsonResponse({'success': 'true'}),
                  'failure': JsonResponse({'success': 'false'})}


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = BasicIngredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ['^name']
    filter_backends = (filters.SearchFilter,)


class UserFollowingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrSuperuserOrReadOnly,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        author = get_object_or_404(User, username=self.request.data['author'])
        user = serializer.context['request'].user
        try:
            serializer.save(author=author, user=user)
            response = JSON_RESPONSES['success']
        except ValidationError:
            response = JSON_RESPONSES['failure']

        return response

    def destroy(self, request, pk=None):
        author = get_object_or_404(User, username=pk)
        user = request.user
        instance = get_object_or_404(Subscription, author=author, user=user)
        instance.delete()
        return JSON_RESPONSES['success']


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrSuperuserOrReadOnly,)
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        user = serializer.context['request'].user
        try:
            serializer.save(recipe=recipe, user=user)
            response = JSON_RESPONSES['success']
        except ValidationError:
            response = JSON_RESPONSES['failure']

        return response

    def destroy(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        instance = get_object_or_404(Favorite, recipe=recipe, user=user)
        instance.delete()
        return JSON_RESPONSES['success']


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrSuperuserOrReadOnly,)
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        user = serializer.context['request'].user
        try:
            serializer.save(recipe=recipe, user=user)
            response = JSON_RESPONSES['success']
        except ValidationError:
            response = JSON_RESPONSES['failure']

        return response

    def destroy(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        instance = get_object_or_404(Purchase, recipe=recipe, user=user)
        instance.delete()
        return JSON_RESPONSES['success']
