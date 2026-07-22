from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('menu/category/<int:id>/', views.menu_category, name='menu_category'),
    path("food/<int:id>/", views.food_details, name="food_details"),
]