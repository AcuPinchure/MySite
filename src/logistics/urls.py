from django.urls import path, include, re_path
from . import views
from django.views.generic import RedirectView

app_name = "logistics"

order_patterns = [
    path('', views.order, name='order'),
    path('edit/<str:order_uuid>/', views.orderEdit, name='order_edit'),
]

urlpatterns = [
    path('home/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('order/', include(order_patterns)),
    path('delivery/', views.delivery, name='delivery'),
    re_path(r'^.?', RedirectView.as_view(
        pattern_name='logistics:home', permanent=False))
]
