from django.shortcuts import render, redirect
from django.contrib import auth

from .models import Account, Order

# Create your views here.


def login(request):

    return render(request, 'logistics/login.html')


def home(request):
    curr_user = auth.get_user(request)

    # if account exists
    if Account.objects.filter(user=curr_user).exists():
        the_account = Account.objects.get(user=curr_user)
    else:
        the_account = Account.objects.create(
            user=curr_user,
            name="未命名"
        )
        the_account.save()

    # render html
    # get order info
    order_unsend = len(Order.objects.filter(
        owner=the_account, delivery_status="未出貨"))
    order_sending = len(Order.objects.filter(
        owner=the_account, delivery_status="已出貨"))

    return render(
        request, 'logistics/home.html',
        {
            "order_unsend": order_unsend,
            "order_sending": order_sending
        })


def account(request):
    return render(request, 'logistics/account.html')


def warehouse(request):
    return render(request, 'logistics/warehouse/warehouse.html')


def order(request):
    if request.method == "POST":
        post = request.POST
        action = list(post.keys())[-1]
        if action == "new_order":
            return redirect("logistics:order_edit", order_uuid="1234")
    return render(request, 'logistics/order/order.html')


def orderEdit(request, order_uuid):
    return render(request, 'logistics/order/order_edit.html', {
        "order_id": order_uuid
    })


def delivery(request):
    return render(request, 'logistics/delivery.html')
