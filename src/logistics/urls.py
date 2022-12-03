from django.urls import path, include, re_path
from . import views
from django.views.generic import RedirectView

app_name = "logistics"

login_patterns = [
    path('', views.welcome, name='login'),
    path('checkExists/', views.checkUserExists, name="check_user_exists")
]

order_patterns = [
    path('<str:order_filter>/', views.order, name='order'),
    path('edit/<str:order_uuid>/', views.orderEdit, name='order_edit'),
]

urlpatterns = [
    path('login/', include(login_patterns)),
    path('logout/', views.toWelcome, name="logout"),
    path('home/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('warehouse/<str:item_sort>', views.warehouse, name='warehouse'),
    path('order/', include(order_patterns)),
    path('delivery/', views.delivery, name='delivery'),
    re_path(r'^.?', RedirectView.as_view(
        pattern_name='logistics:login', permanent=False))
]
