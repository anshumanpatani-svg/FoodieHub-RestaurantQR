from django.shortcuts import render, redirect, get_object_or_404
from .models import Bill


def billing_dashboard(request):

    bills = Bill.objects.filter(
        payment_status="Unpaid"
    )

    return render(
        request,
        "billing_dashboard.html",
        {
            "bills": bills
        }
    )


def invoice(request, id):

    bill = get_object_or_404(
        Bill,
        id=id
    )

    return render(
        request,
        "invoice.html",
        {
            "bill": bill
        }
    )


def mark_paid(request, id):

    bill = get_object_or_404(
        Bill,
        id=id
    )

    bill.payment_status = "Paid"

    bill.save()

    bill.order.status = "Completed"

    bill.order.save()

    return redirect("billing_dashboard")