from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('shopping/', views.shop_list, name='shop_list'),
    path('shopping/download/', views.get_purchases, name='get_purchases'),
]
