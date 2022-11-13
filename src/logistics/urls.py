from django.urls import path, include, re_path
from . import views
from django.views.generic import RedirectView

app_name = "logistics"
urlpatterns = [
    path('home/', views.home, name='home'),
    re_path(r'^.?',RedirectView.as_view(pattern_name='logistics:home', permanent=False))
]
