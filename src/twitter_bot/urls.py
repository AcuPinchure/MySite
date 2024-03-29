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
    path('get/', api_views.getFollowers, name="get_followers"),
]

detail_stats_api_endpoints = [
    path('posts/', api_views.getPostDetail, name="get_post_detail"),
    path('likes/', api_views.getLikeDetail, name="get_like_detail"),
    path('rts/', api_views.getRtDetail, name="get_rt_detail"),
]

config_endpoints = [
    path('get/', api_views.getServiceConfig, name="get_config"),
    path('update/<str:id_name>/',
         api_views.updateServiceConfig, name="update_config"),
]

image_api_endpoints = [
    path('list/', api_views.listImages, name="list_images"),
    path('get/<int:pk>/', api_views.getImageDetail, name="get_image"),
    path('setWeight/<int:pk>/', api_views.setImageWeight, name="set_image_weight"),
]

api_endpoints = [
    path('getStats/', api_views.getStats, name="get_stats"),
    path('detailStats/', include(detail_stats_api_endpoints)),
    path('loadDefaultStats/', api_views.loadDefaultStats,
         name="load_default_stats"),
    path('config/', include(config_endpoints)),
    path('tweet/', include(tweet_api_endpoints)),
    path('image/', include(image_api_endpoints)),
    path('followers/', include(followers_api_endpoints)),
    path('testLogin/', api_views.testLogin, name="test_login"),
    path('testAuth/', api_views.testAuth, name="test_auth"),
]


urlpatterns = [
    path('', views.index, name='about'),
    path('stats/', views.index, name='stats'),
    path('status/', views.index, name='status'),
    path('login/', views.indexLogin, name='login'),
    path('logout/', views.indexLogout, name='logout'),
    path('config/', views.indexLoginRequired, name='config'),
    path('library/', views.indexLoginRequired, name='library'),
    path('logs/', views.indexLoginRequired, name='logs'),
    path('api/', include(api_endpoints)),
    re_path(r'.*', views.notFound),
]
