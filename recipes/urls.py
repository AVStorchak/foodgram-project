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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
