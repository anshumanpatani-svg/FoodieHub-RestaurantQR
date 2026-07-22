from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Food


def home(request):

    categories = Category.objects.all()

    foods = Food.objects.filter(available=True)

    search = request.GET.get("q")

    if search:
        foods = foods.filter(
            Q(food_name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    return render(request, "home.html", {
        "categories": categories,
        "foods": foods,
        "search": search
    })


def menu(request):

    categories = Category.objects.all()

    foods = Food.objects.filter(available=True)

    search = request.GET.get("q")

    if search:
        foods = foods.filter(
            Q(food_name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    return render(request, "menu.html", {
        "categories": categories,
        "foods": foods,
        "search": search
    })


def menu_category(request, id):

    categories = Category.objects.all()

    foods = Food.objects.filter(
        category_id=id,
        available=True
    )

    search = request.GET.get("q")

    if search:
        foods = foods.filter(
            Q(food_name__icontains=search) |
            Q(description__icontains=search)
        )

    return render(request, "menu.html", {
        "categories": categories,
        "foods": foods,
        "search": search
    })


def food_details(request, id):

    food = get_object_or_404(
        Food,
        id=id,
        available=True
    )

    return render(request, "food_details.html", {
        "food": food
    })