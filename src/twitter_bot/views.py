from django.shortcuts import render, redirect
from django.http import HttpResponse
from pathlib import Path
import os
from .models import Seiyuu, WeeklyStats, Tweet, UserAccount

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