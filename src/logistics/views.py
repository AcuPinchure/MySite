# basic functions
from django.shortcuts import render, redirect
from datetime import datetime

# ajax
import json
from django.http import HttpResponse

# auth
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# models
from .models import Account, Order, Item, Storage, Delivery

# Create your views here.


def welcome(request):
    # logout(request)

    form = UserCreationForm()

    error_msg = ""

    if request.method == "POST":
        post = request.POST
        print(post)
        action = list(post.keys())[-1]
        if action == "login":
            username = post['user_id']
            pwd = post['user_pwd']
            curr_user = authenticate(
                username=username, password=pwd)
            # print(curr_user)
            if curr_user and curr_user.is_active:
                login(request, curr_user)
            else:
                error_msg = "帳號或密碼輸入錯誤"
        elif action == "register":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                curr_user = form.save()

    # if user is already logged in
    # skip login page
    if request.user.is_authenticated:
        return redirect('logistics:home')

    return render(
        request, 'logistics/login.html',
        {
            "error_msg": error_msg,
            "form": form
        })


@login_required
def toWelcome(request):
    logout(request)
    return redirect('logistics:login')

# ajax


def checkUserExists(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        try_name = request.POST['try_name']
        if User.objects.filter(username=try_name).exists():
            exists = True
        else:
            exists = False
        print(exists)
        return HttpResponse(json.dumps({
            "exists": exists
        }, ensure_ascii=False), content_type="application/json")

    return redirect('logistics:login')


@login_required
def home(request):
    curr_user = auth.get_user(request)

    # if account exists
    if Account.objects.filter(user=curr_user).exists():
        the_account = Account.objects.get(user=curr_user)
    else:
        return redirect("logistics:account")

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
            "order_sending": order_sending,
            "the_account": the_account
        })


@login_required
def account(request):
    curr_user = auth.get_user(request)

    if request.method == "POST":
        post = request.POST
        print(post)
        action = list(post.keys())[-1]
        if action == "account_edit":
            the_account = Account.objects.get(user=curr_user)
            the_account.name = post['account_name']
            the_account.bank_id = post['bank_id']
            the_account.account_id = post['bank_account_id']
            if request.FILES:
                the_account.profile_image = request.FILES['profile_image']
            the_account.save()

    # if account exists
    if Account.objects.filter(user=curr_user).exists():
        the_account = Account.objects.get(user=curr_user)
    else:
        the_account = Account.objects.create(
            user=curr_user,
            name="未命名"
        )
        the_account.save()
    return render(
        request, 'logistics/account.html',
        {
            "the_account": the_account
        })


@login_required
def warehouse(request):
    return render(request, 'logistics/warehouse/warehouse.html')


@login_required
def order(request):
    curr_user = auth.get_user(request)
    # if account exists
    if Account.objects.filter(user=curr_user).exists():
        the_account = Account.objects.get(user=curr_user)
    else:
        return redirect("logistics:account")

    order_filter = "all"

    if request.method == "POST":
        post = request.POST
        print(post)
        action = list(post.keys())[-1]
        if action == "new_order":
            new_order = Order.objects.create(
                owner=the_account
            )
            new_order.save()
            return redirect("logistics:order_edit", order_uuid=new_order.uuid)
        elif action == "arrive_order":
            the_order = Order.objects.get(pk=post['order_uuid'])
            the_order.delivery_status = "到達倉庫"
            the_order.save()
        elif action == "departure_order":
            the_order = Order.objects.get(pk=post['order_uuid'])
            the_order.delivery_status = "已出貨"
            the_order.save()
        elif action == "filter_order":
            order_filter = post['filter_order']

    # render
    order_list = []
    if order_filter == "all":
        orders = Order.objects.filter(owner=the_account, delivery_status="未出貨") | Order.objects.filter(
            owner=the_account, delivery_status="已出貨")
    elif order_filter == "not_depart":
        orders = Order.objects.filter(owner=the_account, delivery_status="未出貨")
    elif order_filter == "depart":
        orders = Order.objects.filter(owner=the_account, delivery_status="已出貨")

    for order in orders:
        items = []
        paid = 0
        not_paid = 0
        for item in Item.objects.filter(order=order):
            items.append(item)
            if item.is_paid:
                paid += item.price
            else:
                not_paid += item.price
        order_list.append({
            "order": order,
            "items": items,
            "paid": paid,
            "not_paid": not_paid
        })

    return render(
        request, 'logistics/order/order.html',
        {
            "the_account": the_account,
            "order_list": order_list,
            "order_filter": order_filter
        })


@login_required
def orderEdit(request, order_uuid):
    curr_user = auth.get_user(request)
    # if account exists
    if Account.objects.filter(user=curr_user).exists():
        the_account = Account.objects.get(user=curr_user)
    else:
        return redirect("logistics:account")

    if request.method == "POST":
        post = request.POST
        print(post)
        action = post['action']
        if action == "save_info":
            the_order = Order.objects.get(pk=order_uuid)
            the_order.source = post['order_source']
            the_order.order_id = post['order_id']
            the_order.delivery_status = post['order_status']
            the_order.delivery_cost = post['delivery_cost']
            the_order.delivery_name = post['delivery_name']
            the_order.delivery_id = post['delivery_id']
            the_order.expect_arrival = datetime.strptime(
                post['expect_arrival'], "%Y-%m-%d")
            the_order.save()

        elif action == "save_item":
            item_uuid = post['item_uuid']
            the_item = Item.objects.get(pk=item_uuid)
            the_item.name = post['item_name']
            the_item.count = post['item_count']
            the_item.price = post['item_price']
            if post['item_contractor']:
                the_item.contractor = Account.objects.get(
                    pk=post['item_contractor'])
            the_item.save()

        elif action == "set_paid":
            item_uuid = post['item_uuid']
            the_item = Item.objects.get(pk=item_uuid)
            if post['is_paid'] == "true":
                the_item.is_paid = True
            else:
                the_item.is_paid = False
            the_item.save()

        elif action == "save_item_new":
            the_item = Item.objects.create(
                name=post['item_name'],
                count=int(post['item_count']),
                price=int(post['item_price']),
                is_paid=False,
                order=Order.objects.get(pk=order_uuid),
                contractor=Account.objects.get(
                    pk=post['item_contractor'])
            )
            the_item.save()

        elif action == "del_order":
            the_order = Order.objects.get(pk=order_uuid)

            # del items
            for item in Item.objects.filter(order=the_order):
                item.delete()
            the_order.delete()
            return redirect("logistics:order")

    # render
    the_order = Order.objects.get(pk=order_uuid)
    items = list(Item.objects.filter(order=the_order))
    accounts = list(Account.objects.all().exclude(user=curr_user))

    return render(request, 'logistics/order/order_edit.html', {
        "the_account": the_account,
        "the_order": the_order,
        "items": items,
        "accounts": accounts
    })


@login_required
def delivery(request):
    return render(request, 'logistics/delivery.html')
