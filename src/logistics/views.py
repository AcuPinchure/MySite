from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'logistics/home.html')


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
