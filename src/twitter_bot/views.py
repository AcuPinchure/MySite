from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pathlib import Path
import os
from django.conf import settings

# models and query
from .models import Seiyuu, WeeklyStats, Tweet, UserAccount, Followers
from django.db.models import Avg, Count, Sum

# rest framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# time utils
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

# Create your views here.
root_path = Path(__file__).resolve().parent.parent.parent

def index(request):
    return render(request,'twitter_bot/index.html')

def about(request):
    return render(request,'twitter_bot/about.html')

def log(request):
    log_list = os.listdir(os.path.join(root_path,"crontabLog"))
    
    return render(request, 'twitter_bot/log.html', {
        'log_list': log_list
    })

def log_content(request, log_name):
    with open(os.path.join(root_path,"crontabLog",log_name),"r") as log_in:
        log_content = log_in.readlines()
    
    return render(request, 'twitter_bot/log_content.html', {
        'log_name': log_name,
        'log_content': log_content
    })

def stats(request):
    return render(request, 'twitter_bot/stats/stats.html')


# rest framework

@api_view(['GET'])
def loadDefaultStats(request):
    seiyuu_list = Seiyuu.objects.all().order_by("id")
    default_seiyuu = seiyuu_list.first()
    latest_post = Tweet.objects.filter(media__seiyuu=default_seiyuu,data_time__isnull=False).latest("post_time")

    default_data = {
        "seiyuus": {},
        "default_seiyuu": default_seiyuu.id_name,
        "latest_post_time": latest_post.post_time.strftime("%Y-%m-%d")
    }

    for name, id_name, screen_name in seiyuu_list.values_list("name", "id_name", "screen_name"):
        default_data["seiyuus"][id_name] = {
            "name": name,
            "screen_name": screen_name,
        }

    return Response({"status": True, "data": default_data},status=status.HTTP_200_OK)


@api_view(['GET'])
def getStats(request):
    seiyuu = request.GET.get("seiyuu")
    if not seiyuu in ["kaorin","akarin","chemi"]:
        return Response({'status':False, 'message': 'Requested Seiyuu does not match any'},status=status.HTTP_400_BAD_REQUEST)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status':False, 'message': 'Requested time interval missing'},status=status.HTTP_400_BAD_REQUEST)


    tweet_q = None
    try:
        the_timezone = pytz.timezone(timezone_name)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        start_date = the_timezone.localize(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        end_date = the_timezone.localize(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
        tweet_q = Tweet.objects.filter(media__seiyuu__id_name=seiyuu,post_time__gte=start_date,post_time__lte=end_date,data_time__isnull=False).order_by("data_time")
        follower_q = Followers.objects.filter(seiyuu__id_name=seiyuu,data_time__gte=start_date,data_time__lte=end_date).order_by("data_time")
    except TypeError:
        return Response({'status':False, 'message': 'Requested time interval has incorrect format'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status':False, 'message': 'Unknown exception: {}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not tweet_q:
        return Response({'status':False, 'message': 'No Tweets found in the given interval'}, status=status.HTTP_404_NOT_FOUND)
    
    data = {
        "status": True,
        "start_date": tweet_q.first().post_time.strftime("%Y-%m-%d %H:%M"),
        "end_date": tweet_q.last().post_time.strftime("%Y-%m-%d %H:%M"),
        "interval": (tweet_q.last().post_time - tweet_q.first().post_time) / timedelta(hours=1),
        "posts": tweet_q.count(),
        "likes": tweet_q.aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
        "rts": tweet_q.aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,
        "top_likes": [],
        "top_rts": [],
        "seiyuu": seiyuu,
    }

    top_like_id_list = tweet_q.order_by('-like')[:10].values_list("id", flat=True)
    data["top_likes"] = list(map(str, top_like_id_list))
    top_rt_id_list = tweet_q.order_by('-rt')[:10].values_list("id", flat=True)
    data["top_rts"] = list(map(str, top_rt_id_list))

    followers = []

    for date, follower in follower_q.values_list("data_time","followers"):
        followers.append({
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "followers": follower
        })

    data["followers"] = followers




    return Response(data,status=status.HTTP_200_OK)

            
@api_view(['GET'])
def getNoDataTweets(request):
    if request.get_host() in settings.LOCAL_HOSTS:

        no_data_tweets = Tweet.objects.select_related('media__seiyuu')

        time_buffer = 24 # hours

        no_data_tweets = no_data_tweets.filter(data_time__isnull=True,post_time__lte=timezone.now()-timedelta(hours=time_buffer)).order_by("post_time")

        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            no_data_tweets = no_data_tweets[:limit]

        data = no_data_tweets.values('id', 'post_time', 'media__seiyuu__screen_name')

        return Response(data,status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not allowed host name"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['PUT'])
def updateTweetData(request, pk):
    if request.get_host() in settings.LOCAL_HOSTS:
        try:
            # Retrieve the object you want to update based on the 'pk' parameter
            the_tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            return Response({"message": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract the data from the PUT request using request.data
        data = request.data

        # Update the fields of the object with the data from the request
        the_tweet.data_time = timezone.now()
        the_tweet.like = data.get('like')
        the_tweet.rt = data.get('rt')
        #the_tweet.reply = data.get('reply')
        the_tweet.quote = data.get('quote')
        # Add more fields as needed

        # Save the updated object to the database
        the_tweet.save()

        return Response({"message": "Object updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not allowed host name"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
def setFollowers(request):
    if request.get_host() in settings.LOCAL_HOSTS:

        # Extract the data from the POST request using request.data
        data = request.data

        Followers.objects.create(
            data_time=timezone.now(),
            seiyuu=Seiyuu.objects.get(screen_name=data.get('seiyuu')),
            followers=int(data.get('followers'))
        )

        return Response({"message": "Object create successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not allowed host name"}, status=status.HTTP_403_FORBIDDEN)