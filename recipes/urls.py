from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'profile/<str:username>/<int:recipe_id>/',
        views.recipe_view,
        name='recipe'
    ),
    path(
        'profile/<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'profile/<str:username>/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('shopping/', views.shop_list, name='shop_list'),
    path('shopping/download/', views.get_purchases, name='get_purchases'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
