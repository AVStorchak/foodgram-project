from django.urls import path

from . import views

app_name = 'about'


urlpatterns = [
    path('author/', views.AuthorFlatPage.as_view(), name='author'),
    path('tech/', views.TechFlatPage.as_view(), name='tech'),
]