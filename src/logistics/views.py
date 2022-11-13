from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'logistics/home.html')

def account(request):
    return render(request, 'logistics/account.html')

def warehouse(request):
    return render(request, 'logistics/warehouse.html')

def order(request):
    return render(request, 'logistics/order.html')

def delivery(request):
    return render(request, 'logistics/delivery.html')
