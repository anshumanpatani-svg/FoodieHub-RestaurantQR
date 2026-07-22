from django.shortcuts import render, redirect, get_object_or_404

from orders.models import Order
from django.http import JsonResponse
from orders.models import Order



def dashboard(request):

    orders = Order.objects.exclude(status="Completed").order_by("-id")

    return render(
        request,
        "kitchen_dashboard.html",
        {
            "orders": orders
        }
    )


def change_status(request, id, status):

    order = get_object_or_404(Order, id=id)

    order.status = status

    order.save()

    return redirect("kitchen_dashboard")


def notification_count(request):
    count = Order.objects.filter(status="Pending").count()
    latest = Order.objects.order_by("-id").first()

    return JsonResponse({
        "count": count,
        "latest": latest.id if latest else 0,
    })
