from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('log/', views.log, name='log'),
    path('log/<str:log_name>', views.log_content, name='log_content'),
    path('stats/<str:name>', views.stats, name='stats')
]