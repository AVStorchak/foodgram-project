from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, PurchaseViewSet,
                    UserFollowingViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('subscribe', UserFollowingViewSet)
router.register('favorites', FavoriteViewSet)
router.register('purchases', PurchaseViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
