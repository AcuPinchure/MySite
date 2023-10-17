from django.urls import path, include
from . import views

app_name = 'bot'

tweet_api_endpoints = [
    path('noData/', views.getNoDataTweets, name="no_data_tweets"),
    path('updateData/<int:pk>/', views.updateTweetData, name="update_tweet_data"),
]

followers_api_endpoints = [
    path('set/', views.setFollowers, name="set_followers"),
]

api_endpoints = [
    path('getStats/', views.getStats, name="get_stats"),
    path('loadDefaultStats/', views.loadDefaultStats, name="load_default_stats"),
    path('tweet/', include(tweet_api_endpoints)),
    path('followers/', include(followers_api_endpoints))
]


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('log/', views.log, name='log'),
    path('log/<str:log_name>', views.log_content, name='log_content'),
    path('stats/', views.stats, name='stats'),
    path('api/', include(api_endpoints))
]