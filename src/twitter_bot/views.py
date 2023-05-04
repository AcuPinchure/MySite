from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pathlib import Path
import os

# models and query
from .models import Seiyuu, WeeklyStats, Tweet, UserAccount
from django.db.models import Avg, Count, Sum

# rest framework
from .serializer import TweetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from datetime import datetime

# Create your views here.
root_path = Path(__file__).resolve().parent.parent.parent

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

def stats(request, name):
    the_seiyuu = Seiyuu.objects.get(id_name=name)

    the_week_data = WeeklyStats.objects.filter(seiyuu=the_seiyuu).latest("end_date")
    the_last_week_data = WeeklyStats.objects.filter(seiyuu=the_seiyuu).order_by("-end_date")[1]
    the_earliest_data = WeeklyStats.objects.filter(seiyuu=the_seiyuu).earliest("end_date")

    # render
    render_data = {
        "screen_name": the_seiyuu.screen_name,
        "name": the_seiyuu.name,
        "week_data": {
            "earliest_date": the_earliest_data.start_date.strftime("%Y/%m/%d"),
            "start_date": the_week_data.start_date.strftime("%Y/%m/%d"),
            "end_date": the_week_data.end_date.strftime("%Y/%m/%d"),
            "posts": the_week_data.posts,
            "likes": the_week_data.likes,
            "rts": the_week_data.rts,
            "avg_likes": the_week_data.avg_likes,
            "avg_retweets": the_week_data.avg_retweets,
            "max_likes_id": the_week_data.max_likes.id,
            "max_rts_id": the_week_data.max_rts.id,
            "posts_all": the_week_data.posts_all,
            "likes_all": the_week_data.likes_all,
            "rts_all": the_week_data.rts_all,
            "max_likes_all_id": the_week_data.max_likes_all.id,
            "max_rt_all_id": the_week_data.max_rt_all.id,
            "follower_diff": the_week_data.follower - the_last_week_data.follower,
            "total_follower": the_week_data.follower
        }
    }



    return render(request, 'twitter_bot/stats/stats_base.html', render_data)


# rest framework

@api_view(['GET'])
def getStats(request):
    if request.method == 'GET':

        seiyuu = request.GET.get("seiyuu")
        if not seiyuu in ["Kaorin","Akarin","Chemi"]:
            return Response({'status':False, 'message': 'Requested Seiyuu does not match any'},status=status.HTTP_400_BAD_REQUEST)

        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")
        if not (start_date_str and end_date_str):
            return Response({'status':False, 'message': 'Requested time interval missing'},status=status.HTTP_400_BAD_REQUEST)

        tweet_q = None
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999)
            tweet_q = Tweet.objects.filter(post_time__gte=start_date,post_time__lte=end_date,data_time__isnull=False).order_by("data_time")
        except TypeError:
            return Response({'status':False, 'message': 'Requested time interval has incorrect format'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':False, 'message': 'Unknown exception: {}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not tweet_q:
            return Response({'status':False, 'message': 'No Tweets found in the given interval'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "status": True,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "posts": tweet_q.count(),
            "likes": tweet_q.aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
            "rts": tweet_q.aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,
            "avg_likes": tweet_q.aggregate(avg_likes=Avg('like'))['avg_likes'] or 0,
            "avg_retweets": tweet_q.aggregate(avg_rts=Avg('rt'))['avg_rts'] or 0,
            "max_likes": tweet_q.order_by('-like').first().id,
            "max_rts": tweet_q.order_by('-rt').first().id,
            "seiyuu": seiyuu,
        }

        followers = []

        for date, follower in tweet_q.values_list("data_time","follower"):
            followers.append({
                "date": date.strftime("%Y-%m-%d"),
                "followers": follower
            })

        data["followers"] = followers




        return Response(data,status=status.HTTP_200_OK)

            
        