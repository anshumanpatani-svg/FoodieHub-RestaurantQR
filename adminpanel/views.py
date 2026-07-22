from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect ,get_object_or_404

from menu.models import Food, Category
from orders.models import *
from billing.models import Bill
from menu.models import Food
from .forms import *

import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required(login_url='login')
def dashboard(request):

    context = {

        "total_foods": Food.objects.count(),

        "total_categories": Category.objects.count(),

        "total_tables": RestaurantTable.objects.count(),

        "total_orders": Order.objects.count(),

        "pending_orders": Order.objects.filter(status="Pending").count(),

        "completed_orders": Order.objects.filter(status="Completed").count(),

        "total_bills": Bill.objects.count(),

    }

    return render(request, "dashboard.html", context)

@login_required(login_url='login')
def food_list(request):
    foods = Food.objects.select_related("category").all()

    return render(request, "food_list.html", {
        "foods": foods
    })

@login_required(login_url='login')
def food_add(request):

    if request.method == "POST":

        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect("food_list")

    else:

        form = FoodForm()

    return render(request, "food_form.html", {
        "form": form
    })


@login_required(login_url='login')
def food_edit(request, id):

    food = get_object_or_404(Food, id=id)

    if request.method == "POST":

        form = FoodForm(
            request.POST,
            request.FILES,
            instance=food
        )

        if form.is_valid():
            form.save()
            return redirect("food_list")

    else:

        form = FoodForm(instance=food)

    return render(
        request,
        "food_form.html",
        {
            "form": form,
            "title": "Edit Food"
        }
    )


@login_required(login_url='login')
def food_delete(request, id):
    food = get_object_or_404(Food, id=id)

    if request.method == "POST":
        food.delete()
        return redirect("food_list")

    return render(
        request,
        "food_confirm_delete.html",
        {"food": food}
    )


@login_required(login_url='login')
def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "category_list.html",
        {
            "categories":categories
        }
    )


@login_required(login_url='login')
def category_add(request):

    if request.method=="POST":

        form=CategoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("category_list")

    else:

        form=CategoryForm()

    return render(
        request,
        "category_form.html",
        {
            "form":form,
            "title":"Add Category"
        }
    )


@login_required(login_url='login')
def category_edit(request,id):

    category=get_object_or_404(
        Category,
        id=id
    )

    if request.method=="POST":

        form=CategoryForm(
            request.POST,
            request.FILES,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect("category_list")

    else:

        form=CategoryForm(
            instance=category
        )

    return render(
        request,
        "category_form.html",
        {
            "form":form,
            "title":"Edit Category"
        }
    )


@login_required(login_url='login')
def category_delete(request,id):

    category=get_object_or_404(
        Category,
        id=id
    )

    if request.method=="POST":

        category.delete()

        return redirect("category_list")

    return render(
        request,
        "category_delete.html",
        {
            "category":category
        }
    )



@login_required(login_url='login')
def table_list(request):

    tables = RestaurantTable.objects.all().order_by("table_number")

    return render(
        request,
        "table_list.html",
        {
            "tables": tables
        }
    )


@login_required(login_url='login')
def table_add(request):

    if request.method == "POST":

        form = TableForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("table_list")

    else:

        form = TableForm()

    return render(
        request,
        "table_form.html",
        {
            "form": form,
            "title": "Add Table"
        }
    )

@login_required(login_url='login')
def table_edit(request, id):

    table = get_object_or_404(
        RestaurantTable,
        id=id
    )

    if request.method == "POST":

        form = TableForm(
            request.POST,
            instance=table
        )

        if form.is_valid():

            form.save()

            return redirect("table_list")

    else:

        form = TableForm(instance=table)

    return render(
        request,
        "table_form.html",
        {
            "form": form,
            "title": "Edit Table"
        }
    )


@login_required(login_url='login')
def table_delete(request, id):

    table = get_object_or_404(
        RestaurantTable,
        id=id
    )

    if request.method == "POST":

        table.delete()

        return redirect("table_list")

    return render(
        request,
        "table_delete.html",
        {
            "table": table
        }
    )



@login_required(login_url='login')
def generate_qr(request, id):
    table = get_object_or_404(RestaurantTable, id=id)

    qr_url = f"{settings.SITE_URL}{reverse('scan_table', args=[table.table_number])}"
    print(qr_url)
    qr = qrcode.make(qr_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    table.qr_code.save(
        f"table_{table.table_number}.png",
        File(buffer),
        save=True
    )

    return redirect("table_list")


@login_required(login_url='login')
def qr_cards(request):

    tables = RestaurantTable.objects.all().order_by("table_number")

    return render(
        request,
        "qr_cards.html",
        {
            "tables": tables
        }
    )



@login_required(login_url='login')
def order_list(request):

    orders = Order.objects.select_related("table").order_by("-order_date")

    search = request.GET.get("search")
    status = request.GET.get("status")
    table = request.GET.get("table")
    today = request.GET.get("today")

    if search:
        orders = orders.filter(
            order_number__icontains=search
        )

    if status:
        orders = orders.filter(status=status)

    if table:
        orders = orders.filter(table_id=table)

    if today == "1":
        today_date = timezone.localdate()
        orders = orders.filter(order_date__date=today_date)

    context = {

        "orders": orders,

        "tables": RestaurantTable.objects.all(),

        "search": search,

        "selected_status": status,

        "selected_table": table,

        "today": today,

        "total_orders": Order.objects.count(),

        "pending_orders": Order.objects.filter(status="Pending").count(),

        "preparing_orders": Order.objects.filter(status="Preparing").count(),

        "ready_orders": Order.objects.filter(status="Ready").count(),

        "completed_orders": Order.objects.filter(status="Completed").count(),

    }

    return render(
        request,
        "orders_list.html",
        context
    )


@login_required(login_url='login')
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    items = OrderItem.objects.filter(
        order=order
    ).select_related("food")

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
            "items": items,
        }
    )


@login_required(login_url='login')
def update_order_status(request, id, status):

    order = get_object_or_404(Order, id=id)

    allowed_status = [
        "Pending",
        "Preparing",
        "Ready",
        "Completed",
    ]

    if status in allowed_status:
        order.status = status
        order.save()

    return redirect("order_detail", id=order.id)


@login_required(login_url='login')
def order_table_ajax(request):

    orders = Order.objects.all().order_by("-order_date")

    search = request.GET.get("search")

    status = request.GET.get("status")

    table = request.GET.get("table")

    today = request.GET.get("today")

    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(table__table_number__icontains=search)
        )

    if status:
        orders = orders.filter(status=status)

    if table:
        orders = orders.filter(table_id=table)

    if today == "1":
        orders = orders.filter(order_date__date=timezone.localdate())

    html = render_to_string(
        "order_table.html",
        {"orders": orders},
        request=request,
    )

    return JsonResponse({"html": html})

