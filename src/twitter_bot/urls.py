from django.urls import path, include, re_path
from . import views, api_views

app_name = 'bot'

tweet_api_endpoints = [
    path('noData/', api_views.getNoDataTweets, name="no_data_tweets"),
    path('updateData/<int:pk>/', api_views.updateTweetData,
         name="update_tweet_data"),
]

followers_api_endpoints = [
    path('set', api_views.setFollowers, name="set_followers"),
]

api_endpoints = [
    path('getStats', api_views.getStats, name="get_stats"),
    path('loadDefaultStats', api_views.loadDefaultStats, name="load_default_stats"),
    path('tweet/', include(tweet_api_endpoints)),
    path('followers/', include(followers_api_endpoints)),
    path('testLogin', api_views.testLogin, name="test_login"),
    path('testAuth', api_views.testAuth, name="test_auth"),
]


urlpatterns = [
    path('', views.index, name='about'),
    path('stats', views.index, name='stats'),
    path('login', views.indexLogin, name='login'),
    path('logout', views.indexLogout, name='logout'),
    path('config', views.indexLoginRequired, name='config'),
    path('library', views.indexLoginRequired, name='library'),
    path('logs', views.indexLoginRequired, name='logs'),
    path('api/', include(api_endpoints)),
    re_path(r'.*', views.notFound),
]
