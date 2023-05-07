from django.urls import path, include
from . import views

app_name = 'bot'

api_patterns = [
    path('getStats/', views.getStats, name="get_stats"),
    path('loadDefaultStats/', views.loadDefaultStats, name="load_default_stats")
]


urlpatterns = [
    path('about/', views.about, name='about'),
    path('log/', views.log, name='log'),
    path('log/<str:log_name>', views.log_content, name='log_content'),
    path('stats/', views.stats, name='stats'),
    path('api/', include(api_patterns))
]