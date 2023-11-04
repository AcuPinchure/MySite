# settings
from django.conf import settings

# rest framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# time utils
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

# models and query
from .models import Seiyuu, Tweet, Followers
from django.db.models import Avg, Count, Sum


@api_view(['POST'])
def testLogin(request):
    data = request.data
    print(data)
    # test if data has key "username" and "password"
    if not data.get("username") or not data.get("password"):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # test if user exists
    user = authenticate(username=data.get("username"),
                        password=data.get("password"))
    if not user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def testAuth(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def loadDefaultStats(request):
    """
    get the default data for the dashboard when mounted
    """
    seiyuu_list = Seiyuu.objects.all().order_by("id")
    default_seiyuu = seiyuu_list.first()
    latest_post = Tweet.objects.filter(
        media__seiyuu=default_seiyuu, data_time__isnull=False).latest("post_time")

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

    return Response({"status": True, "data": default_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getStats(request):
    """
    get basic stats for dashboard, given data search interval

    [url params]
    seiyuu: seiyuu id_name
    start_date: start date of the searching interval
    end_date: end date of the searching interval

    [return]
    seiyuu_name: seiyuu name
    seiyuu_id: seiyuu screen name
    start_date: start date of the data interval
    end_date: end date of the data interval
    interval: time interval in hours
    posts: total number of posts
    likes: total number of likes
    rts: total number of retweets
    """
    seiyuu = request.GET.get("seiyuu")
    if not Seiyuu.objects.filter(id_name=seiyuu).exists():
        return Response({'status': False, 'message': 'Requested Seiyuu does not match any'}, status=status.HTTP_400_BAD_REQUEST)

    the_seiyuu = Seiyuu.objects.get(id_name=seiyuu)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status': False, 'message': 'Requested time interval missing'}, status=status.HTTP_400_BAD_REQUEST)

    tweet_q = None
    try:
        the_timezone = pytz.timezone(timezone_name)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        start_date = the_timezone.localize(start_date).replace(
            hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        end_date = the_timezone.localize(end_date).replace(
            hour=23, minute=59, second=59, microsecond=999999)
        tweet_q = Tweet.objects.filter(media__seiyuu=the_seiyuu, post_time__gte=start_date,
                                       post_time__lte=end_date, data_time__isnull=False).order_by("data_time")
    except TypeError:
        return Response({'status': False, 'message': 'Requested time interval has incorrect format'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status': False, 'message': 'Unknown exception: {}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not tweet_q:
        return Response({'status': False, 'message': 'No Tweets found in the given interval'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "status": True,
        "seiyuu_name": the_seiyuu.name,
        "seiyuu_id": the_seiyuu.screen_name,
        "start_date": tweet_q.first().post_time.strftime("%Y-%m-%d %H:%M"),
        "end_date": tweet_q.last().post_time.strftime("%Y-%m-%d %H:%M"),
        "interval": (tweet_q.last().post_time - tweet_q.first().post_time) / timedelta(hours=1),
        "posts": tweet_q.count(),
        "likes": tweet_q.aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
        "rts": tweet_q.aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getFollowers(request):
    """
    get followers for dashboard, given data search interval

    [url params]
    seiyuu: seiyuu id_name
    start_date: start date of the searching interval
    end_date: end date of the searching interval

    [return]
    a list of follower data points, the number of data points is limited to 200 (with even interval)
    @props data_time: when was this follower recorded
    @props followers: the number of followers at that time
    """
    seiyuu = request.GET.get("seiyuu")
    if not Seiyuu.objects.filter(id_name=seiyuu).exists():
        return Response({'status': False, 'message': 'Requested Seiyuu does not match any'}, status=status.HTTP_400_BAD_REQUEST)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status': False, 'message': 'Requested time interval missing'}, status=status.HTTP_400_BAD_REQUEST)
    the_timezone = pytz.timezone(timezone_name)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    start_date = the_timezone.localize(start_date).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    end_date = the_timezone.localize(end_date).replace(
        hour=23, minute=59, second=59, microsecond=999999)

    # get data count to check if data points is more than 200
    the_seiyuu = Seiyuu.objects.get(id_name=seiyuu)
    follower_query = Followers.objects.filter(seiyuu=the_seiyuu, data_time__gte=start_date,
                                              data_time__lte=end_date).order_by("data_time")

    if not follower_query:
        return Response({'status': False, 'message': 'No Followers found in the given interval'}, status=status.HTTP_404_NOT_FOUND)

    # get real start and end date
    start_date = follower_query.first().data_time
    end_date = follower_query.last().data_time
    data_count = follower_query.count()

    # if data points is more than 200, get data with even interval
    if data_count > 200:
        time_anchors = []
        # get time interval in seconds
        interval = (end_date - start_date).total_seconds() / 199
        # get time anchors
        curr_time = start_date
        while curr_time < end_date:
            time_anchors.append(curr_time)
            curr_time += timedelta(seconds=interval)

        time_anchors.append(end_date)

        json_data = []

        curr_diff = None
        prev_diff = None
        prev_data_point = None
        # get data with even interval
        for data_point in follower_query:
            curr_diff = abs(data_point.data_time - time_anchors[0])
            if data_point.data_time > time_anchors[0]:
                if prev_diff and curr_diff > prev_diff:
                    json_data.append({
                        "data_time": prev_data_point.data_time.strftime("%Y-%m-%d %H:%M"),
                        "followers": prev_data_point.followers,
                    })
                time_anchors.pop(0)
            prev_diff = curr_diff
            prev_data_point = data_point
    else:
        json_data = follower_query.values(
            'data_time', 'followers').order_by("data_time")

    if not json_data:
        return Response({'status': False, 'message': 'No Followers found in the given interval'}, status=status.HTTP_404_NOT_FOUND)

    return Response({"status": True, "data": json_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPostDetail(request):
    """
    get post detail for dashboard, when user clicks the post data block

    [url params]
    seiyuu: seiyuu id_name
    start_date: start date of the searching interval
    end_date: end date of the searching interval

    [return]
    start_date: start date of the data interval
    end_date: end date of the data interval
    interval: time interval in hours
    posts: total number of posts
    scheduled_interval: scheduled time interval in hours, from service config
    actual_interval: actual time interval in hours, from data
    is_active: if the service is active
    """
    seiyuu = request.GET.get("seiyuu")
    if not Seiyuu.objects.filter(id_name=seiyuu).exists():
        return Response({'status': False, 'message': 'Requested Seiyuu does not match any'}, status=status.HTTP_400_BAD_REQUEST)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status': False, 'message': 'Requested time interval missing'}, status=status.HTTP_400_BAD_REQUEST)

    the_timezone = pytz.timezone(timezone_name)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    start_date = the_timezone.localize(start_date).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    end_date = the_timezone.localize(end_date).replace(
        hour=23, minute=59, second=59, microsecond=999999)

    the_seiyuu = Seiyuu.objects.get(id_name=seiyuu)
    tweet_query = Tweet.objects.filter(media__seiyuu=the_seiyuu, post_time__gte=start_date,
                                       post_time__lte=end_date, data_time__isnull=False).order_by("data_time")

    if not tweet_query:
        return Response({'status': False, 'message': 'No Posts found in the given interval'}, status=status.HTTP_404_NOT_FOUND)

    interval = (tweet_query.last().post_time -
                tweet_query.first().post_time) / timedelta(hours=1)
    posts = tweet_query.count()

    json_data = {
        "status": True,
        "start_date": tweet_query.first().post_time.strftime("%Y-%m-%d %H:%M"),
        "end_date": tweet_query.last().post_time.strftime("%Y-%m-%d %H:%M"),
        "interval": interval,
        "posts": posts,
        "scheduled_interval": the_seiyuu.interval,
        "actual_interval": interval / posts,
        "is_active": the_seiyuu.activated,
    }

    return Response(json_data, status=status.HTTP_200_OK)


def toString(number):
    return str(number)


@api_view(['GET'])
def getLikeDetail(request):
    """
    get like detail for dashboard, when user clicks the like data block

    [url params]
    seiyuu: seiyuu id_name
    start_date: start date of the searching interval
    end_date: end date of the searching interval

    [return]
    start_date: start date of the data interval
    end_date: end date of the data interval
    likes: total number of likes
    avg_likes: average number of likes
    max_likes: a list of the ids of top 10 tweets with the highest number of likes
    """
    seiyuu = request.GET.get("seiyuu")
    if not Seiyuu.objects.filter(id_name=seiyuu).exists():
        return Response({'status': False, 'message': 'Requested Seiyuu does not match any'}, status=status.HTTP_400_BAD_REQUEST)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status': False, 'message': 'Requested time interval missing'}, status=status.HTTP_400_BAD_REQUEST)
    the_timezone = pytz.timezone(timezone_name)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    start_date = the_timezone.localize(start_date).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    end_date = the_timezone.localize(end_date).replace(
        hour=23, minute=59, second=59, microsecond=999999)

    the_seiyuu = Seiyuu.objects.get(id_name=seiyuu)
    tweet_query = Tweet.objects.filter(media__seiyuu=the_seiyuu, post_time__gte=start_date,
                                       post_time__lte=end_date, data_time__isnull=False).order_by("data_time")

    json_data = {
        "status": True,
        "start_date": tweet_query.first().post_time.strftime("%Y-%m-%d %H:%M"),
        "end_date": tweet_query.last().post_time.strftime("%Y-%m-%d %H:%M"),
        "likes": tweet_query.aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
        "avg_likes": tweet_query.aggregate(avg_likes=Avg('like'))['avg_likes'] or 0,
        "max_likes": map(toString, tweet_query.order_by('-like').values_list('id', flat=True)[:10]),
    }

    return Response(json_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRtDetail(request):
    """
    get retweet detail for dashboard, when user clicks the retweet data block

    [url params]
    seiyuu: seiyuu id_name
    start_date: start date of the searching interval
    end_date: end date of the searching interval

    [return]
    start_date: start date of the data interval
    end_date: end date of the data interval
    rts: total number of retweets
    avg_rts: average number of retweets
    max_rts: a list of the ids of top 10 tweets with the highest number of retweets
    """
    seiyuu = request.GET.get("seiyuu")
    if not Seiyuu.objects.filter(id_name=seiyuu).exists():
        return Response({'status': False, 'message': 'Requested Seiyuu does not match any'}, status=status.HTTP_400_BAD_REQUEST)

    timezone_name = request.META.get('TIME_ZONE', 'Asia/Taipei')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if not (start_date_str and end_date_str):
        return Response({'status': False, 'message': 'Requested time interval missing'}, status=status.HTTP_400_BAD_REQUEST)
    the_timezone = pytz.timezone(timezone_name)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    start_date = the_timezone.localize(start_date).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    end_date = the_timezone.localize(end_date).replace(
        hour=23, minute=59, second=59, microsecond=999999)

    the_seiyuu = Seiyuu.objects.get(id_name=seiyuu)
    tweet_query = Tweet.objects.filter(media__seiyuu=the_seiyuu, post_time__gte=start_date,
                                       post_time__lte=end_date, data_time__isnull=False).order_by("data_time")
    json_data = {
        "status": True,
        "start_date": tweet_query.first().post_time.strftime("%Y-%m-%d %H:%M"),
        "end_date": tweet_query.last().post_time.strftime("%Y-%m-%d %H:%M"),
        "rts": tweet_query.aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,
        "avg_rts": tweet_query.aggregate(avg_rts=Avg('rt'))['avg_rts'] or 0,
        "max_rts": map(toString, tweet_query.order_by('-rt').values_list('id', flat=True)[:10]),
    }

    return Response(json_data, status=status.HTTP_200_OK)


########### local api ############


@api_view(['GET'])
def getNoDataTweets(request):
    """
    get all tweets that has not been analyzed, api for local only

    [url params]
    limit: limit number of tweets to return, to prevent twitter from blocking

    [return]
    id: tweet id
    post_time: tweet post time
    seiyuu: seiyuu screen name

    """
    if request.get_host() in settings.LOCAL_HOSTS:

        no_data_tweets = Tweet.objects.select_related('media__seiyuu')

        time_buffer = 72  # hours

        no_data_tweets = no_data_tweets.filter(data_time__isnull=True, post_time__lte=timezone.now(
        )-timedelta(hours=time_buffer)).order_by("post_time")

        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            no_data_tweets = no_data_tweets[:limit]

        data = no_data_tweets.values(
            'id', 'post_time', 'media__seiyuu__screen_name')

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not allowed host name"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
def updateTweetData(request, pk):
    """
    write data to a tweet, api for local only

    [body params]
    data_time: data collection time
    like: number of likes
    rt: number of retweets
    quote: number of quotes
    """
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
        # the_tweet.reply = data.get('reply')
        the_tweet.quote = data.get('quote')
        # Add more fields as needed

        # Save the updated object to the database
        the_tweet.save()

        return Response({"message": "Object updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not allowed host name"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def setFollowers(request):
    """
    write current followers to database, api for local only

    [body params]
    seiyuu: seiyuu screen_name
    followers: number of followers
    """
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
