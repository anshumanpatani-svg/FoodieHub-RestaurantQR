from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantTable, Order, OrderItem
from billing.models import Bill
from menu.models import Food
from django.http import JsonResponse


def scan_table(request, table_number):

    table = get_object_or_404(
        RestaurantTable,
        table_number=table_number
    )

    request.session["table_id"] = table.id
    request.session["table_number"] = table.table_number

    return redirect("home")

def add_to_cart(request, id):

    cart = request.session.get("cart", {})

    id = str(id)

    if id in cart:

        cart[id]["quantity"] += 1

    else:

        cart[id] = {
            "quantity": 1
        }

    request.session["cart"] = cart

    return redirect("cart")


def cart(request):

    cart = request.session.get("cart", {})

    cart_items = []

    total = Decimal("0.00")

    for food_id, item in cart.items():

        food = Food.objects.get(id=food_id)

        subtotal = food.price * item["quantity"]

        total += subtotal

        cart_items.append({
            "food": food,
            "quantity": item["quantity"],
            "subtotal": subtotal
        })

    gst = total * Decimal("0.05")
    grand_total = total + gst

    context = {
        "cart_items": cart_items,
        "subtotal": total,
        "gst": gst,
        "grand_total": grand_total
    }

    return render(request, "cart.html", context)


def increase_cart(request, id):

    cart = request.session.get("cart", {})

    id = str(id)

    if id in cart:
        cart[id]["quantity"] += 1

    request.session["cart"] = cart

    return redirect("cart")


def decrease_cart(request, id):

    cart = request.session.get("cart", {})

    id = str(id)

    if id in cart:

        if cart[id]["quantity"] > 1:

            cart[id]["quantity"] -= 1

        else:

            del cart[id]

    request.session["cart"] = cart

    return redirect("cart")


def remove_cart(request, id):

    cart = request.session.get("cart", {})

    id = str(id)

    if id in cart:

        del cart[id]

    request.session["cart"] = cart

    return redirect("cart")



def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    table_id = request.session.get("table_id")

    if table_id is None:
        return redirect("home")

    table = RestaurantTable.objects.get(id=table_id)

    total = Decimal("0.00")

    for food_id, item in cart.items():
        food = Food.objects.get(id=food_id)
        total += food.price * item["quantity"]

    gst = total * Decimal("0.05")
    grand_total = total + gst

    last_order = Order.objects.order_by("-id").first()

    if last_order:
        next_number = last_order.id + 1001
    else:
        next_number = 1001

    order = Order.objects.create(
        table=table,
        order_number=f"ORD{next_number}",
        total_amount=grand_total,
        status="Pending"
    )

    # ✅ Save order ID in session
    request.session["order_id"] = order.id

    for food_id, item in cart.items():
        food = Food.objects.get(id=food_id)

        OrderItem.objects.create(
            order=order,
            food=food,
            quantity=item["quantity"],
            price=food.price,
            subtotal=food.price * item["quantity"]
        )

    Bill.objects.create(
        order=order,
        subtotal=total,
        gst=gst,
        grand_total=grand_total,
        payment_method="Cash",
        payment_status="Unpaid"
    )

    del request.session["cart"]

    return redirect("order_success", order.id)



def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "order_success.html",
        {
            "order": order
        }
    )



def track_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "track_order.html",
        {
            "order": order
        }
    )




def order_status_api(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return JsonResponse({
        "status": order.status,
        "order_number": order.order_number,
        "table": order.table.table_number,
        "total": str(order.total_amount),
        "date": order.order_date.strftime("%d %b %Y"),
        "time": order.order_date.strftime("%I:%M %p"),
    })