from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from recipes.models import (BasicIngredient, Favorite, Purchase, Recipe,
                            Subscription)

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
        user = serializer._user(obj=None)
        if user != author:
            subscription = Subscription.objects.filter(author=author, user=user)
            if len(subscription) == 0:
                serializer.save(author=author, user=user)
                response = JSON_RESPONSES['success']
            else:
                response = JSON_RESPONSES['failure']
        else:
            response = JSON_RESPONSES['failure']
        return response

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['pk'])
        user = request.user
        instance = get_object_or_404(Subscription.objects, author=author, user=user)
        instance.delete()
        response = JSON_RESPONSES['success']
        return response


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrSuperuserOrReadOnly,)
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        user = serializer._user(obj=None)
        favorite = Favorite.objects.filter(recipe=recipe, user=user)
        if len(favorite) == 0:
            serializer.save(recipe=recipe, user=user)
            response = JSON_RESPONSES['success']
        else:
            response = JSON_RESPONSES['failure']

        return response

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        instance = get_object_or_404(Favorite.objects, recipe=recipe, user=user)
        instance.delete()
        response = JSON_RESPONSES['success']
        return response


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrSuperuserOrReadOnly,)
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        user = serializer._user(obj=None)
        purchase = Purchase.objects.filter(recipe=recipe, user=user)
        if len(purchase) == 0:
            serializer.save(recipe=recipe, user=user)
            response = JSON_RESPONSES['success']
        else:
            response = JSON_RESPONSES['failure']

        return response

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        instance = get_object_or_404(Purchase.objects, recipe=recipe, user=user)
        instance.delete()
        response = JSON_RESPONSES['success']
        return response
