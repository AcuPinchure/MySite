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
from .models import Seiyuu, Tweet, Followers, Media
from django.db.models import Avg, Count, Sum, Max

# serializers
from .serializer import SeiyuuSerializer, MediaSerializer, TweetSerializer

import math


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

        curr_diff = 0
        prev_diff = 0
        prev_data_point = follower_query[0]
        # get data with even interval
        for data_point in follower_query[1:]:
            curr_diff = abs(data_point.data_time - time_anchors[0])
            if data_point.data_time > time_anchors[0]:
                if prev_diff and curr_diff > prev_diff:
                    json_data.append({
                        "data_time": prev_data_point.data_time.strftime("%Y-%m-%d %H:%M"),
                        "followers": prev_data_point.followers,
                    })
                else:
                    json_data.append({
                        "data_time": data_point.data_time.strftime("%Y-%m-%d %H:%M"),
                        "followers": data_point.followers,
                    })
                time_anchors.pop(0)
            prev_diff = curr_diff
            prev_data_point = data_point
        json_data.append({
            "data_time": end_date.strftime("%Y-%m-%d %H:%M"),
            "followers": follower_query.last().followers,
        })
    else:
        json_data = follower_query.values(
            'data_time', 'followers').order_by("data_time")

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


@api_view(['GET'])
def getServiceConfig(request):
    """
    load status of all seiyuu

    [return]
    seiyuu_id_name: seiyuu id_name
    is_active: if the service is active
    interval: time interval in hours
    last_post_time: last post time
    """

    data = []

    # get all seiyuu
    seiyuu_list = Seiyuu.objects.filter(hidden=False).order_by("id")

    return Response({
        "status": True,
        "data": SeiyuuSerializer(seiyuu_list, many=True).data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
def updateServiceConfig(request, id_name):
    """
    update service config

    [url params]
    seiyuu_id_name: seiyuu_id_name

    [body params]
    is_active: if the service is active
    interval: time interval in hours
    """
    # check login
    if not request.user.is_authenticated:
        return Response({"message": "Not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    if not Seiyuu.objects.filter(id_name=id_name).exists():
        return Response({"message": "Seiyuu not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract the data from the PUT request using request.data
    serializer = SeiyuuSerializer(
        data=request.data,
        instance=Seiyuu.objects.get(id_name=id_name)
    )
    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({"message": "Object updated successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def listImages(request):
    """
    list all images in the database

    [url params]
    seiyuu_id_name: seiyuu id_name
    start_date: start date (tweet post time) of the searching interval
    end_date: end date (tweet post time) of the searching interval
    image_start_date: start date (image import time) of the searching interval
    image_end_date: end date (image import time) of the searching interval
    min_likes: minimum number of likes
    max_likes: maximum number of likes
    min_rts: minimum number of retweets
    max_rts: maximum number of retweets
    min_posts: minimum number of posts
    max_posts: maximum number of posts
    tweet_id: tweet id
    page: page number
    order_by: order by, default is "date", options: "date", "likes", "rts", "posts"
    order: order, default is "desc", options: "asc", "desc"

    [return]
    count: total number of images
    total_pages: total number of pages
    data: list of images {
        id: image id
        file: image file
        file_name: image file name
        file_type: image file type
        weight: image weight
        seiyuu: seiyuu id_name
    }
    """
    if not request.user.is_authenticated:
        return Response({"message": "Not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.query_params.get("tweet_id"):
        the_tweet_query = Tweet.objects.filter(
            id=request.query_params.get("tweet_id"))
        if not the_tweet_query.exists():
            return Response({"message": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        the_image = the_tweet_query.first().media
        image_tweet_set_query = Tweet.objects.filter(media=the_image)
        the_image.file_name = the_image.file.name.split('/')[-1]
        the_image.posts = image_tweet_set_query.count()
        the_image.likes = image_tweet_set_query.aggregate(
            max_likes=Max('like'))['max_likes'] or 0
        the_image.rts = image_tweet_set_query.aggregate(
            max_rts=Max('rt'))['max_rts'] or 0

        serializer = MediaSerializer(the_image, many=False)

        return Response({
            "count": 1,
            "total_pages": 1,
            "sort_by": "latest_post_time",
            "order": "desc",
            "page": 1,
            "data": [serializer.data]
        }, status=status.HTTP_200_OK)

    filter_string_list = []

    if request.query_params.get("seiyuu_id_name"):
        filter_string_list.append(
            f"""id_name = '{request.query_params.get("seiyuu_id_name")}'""")

    if request.query_params.get("start_date"):
        filter_string_list.append(
            f"""latest_post_time >= '{request.query_params.get("start_date")}'""")

    if request.query_params.get("end_date"):
        filter_string_list.append(
            f"""earliest_post_time <= '{request.query_params.get("end_date")}'""")

    if request.query_params.get("min_likes"):
        filter_string_list.append(
            f"""likes >= {request.query_params.get("min_likes")}""")

    if request.query_params.get("max_likes"):
        filter_string_list.append(
            f"""likes <= {request.query_params.get("max_likes")}""")

    if request.query_params.get("min_rts"):
        filter_string_list.append(
            f"""rts >= {request.query_params.get("min_rts")}""")

    if request.query_params.get("max_rts"):
        filter_string_list.append(
            f"""rts <= {request.query_params.get("max_rts")}""")

    if request.query_params.get("min_posts"):
        filter_string_list.append(
            f"""posts >= {request.query_params.get("min_posts")}""")

    if request.query_params.get("max_posts"):
        filter_string_list.append(
            f"""posts <= {request.query_params.get("max_posts")}""")

    base_raw_query_command = f"""
            SELECT
                bot_media.id,
                bot_media.file,
                substr(substr(bot_media.file,20), instr(substr(bot_media.file,20), '/') + 1) AS file_name,
                bot_media.file_type,
                bot_media.weight,
                bot_seiyuu.name AS seiyuu_name,
                bot_seiyuu.screen_name AS seiyuu_screen_name,
                bot_seiyuu.id_name AS seiyuu_id_name,
                tweet_latest_time.post_time AS latest_post_time,
                tweet_earliest_time.post_time AS earliest_post_time,
                tweet_post_count.count AS posts,
                tweet_like_count.count AS likes,
                tweet_rt_count.count AS rts
            FROM bot_media
            JOIN bot_seiyuu ON bot_seiyuu.id = bot_media.seiyuu_id
            JOIN 
            (
                SELECT
                    media_id,
                    MAX(post_time) AS post_time
                FROM bot_tweet
                GROUP BY media_id
            )AS tweet_latest_time ON bot_media.id = tweet_latest_time.media_id
            JOIN
            (
                SELECT
                    media_id,
                    MIN(post_time) AS post_time
                FROM bot_tweet
                GROUP BY media_id
            ) AS tweet_earliest_time ON bot_media.id = tweet_earliest_time.media_id
            JOIN
            (
                SELECT
                    media_id, 
                    COUNT(id) AS count
                FROM bot_tweet
                GROUP BY media_id
            ) AS tweet_post_count ON bot_media.id = tweet_post_count.media_id
            JOIN
            (
                SELECT
                    media_id,
                    MAX(bot_tweet."like") AS count
                FROM bot_tweet
                GROUP BY media_id
            ) AS tweet_like_count ON bot_media.id = tweet_like_count.media_id
            JOIN
            (
                SELECT
                    media_id,
                    MAX(bot_tweet.rt) AS count
                FROM bot_tweet
                GROUP BY media_id
            ) AS tweet_rt_count ON bot_media.id = tweet_rt_count.media_id
    """

    if filter_string_list:
        base_raw_query_command += " WHERE " + " AND ".join(filter_string_list)

    base_image_query = Media.objects.raw(base_raw_query_command)

    image_count = len(base_image_query)

    sort_by = request.query_params.get("sort_by", None)
    order = request.query_params.get("order", None)

    if not sort_by in ["latest_post_time", "earliest_post_time", "likes", "rts", "posts"]:
        sort_by = "latest_post_time"
    if not order in ["asc", "desc"]:
        order = "desc"

    raw_query_command_with_order = f"""
        {base_raw_query_command}
        ORDER BY {sort_by} {order.upper()}
    """

    image_query = Media.objects.raw(raw_query_command_with_order)

    page = request.query_params.get("page", None)

    try:
        page = int(page)
    except:
        page = 1

    page_size = 20

    total_pages = math.ceil(image_count / page_size) or 1

    page = min(page, total_pages)

    paginated_serializer = MediaSerializer(
        image_query[(page-1)*page_size:page*page_size], many=True)

    return Response({
        "count": image_count,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "data": paginated_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getImageDetail(request, pk):
    """
    get image detail for dashboard, when user clicks the image data block

    [url params]
    id: image id

    [return]
    {
        id: image id
        file: image file
        file_name: image file name
        file_type: image file type
        weight: image weight
        total_weight: total weight of all images
        seiyuu: seiyuu id_name
        posts: total number of posts
        likes: total number of likes
        rts: total number of retweets
        tweets: [
            {
                id: tweet id
                post_time: tweet post time
                like: number of likes
                rt: number of retweets
                followers: number of followers
            }
        ]
    }
    """
    if not request.user.is_authenticated:
        return Response({"message": "Not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    if not Media.objects.filter(pk=pk).exists():
        return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    the_image = Media.objects.get(pk=pk)
    the_image.file_name = the_image.file.name.split('/')[-1]

    tweet_query = Tweet.objects.filter(media=the_image).order_by("post_time")
    the_image.posts = tweet_query.count()
    the_image.likes = tweet_query.aggregate(max_likes=Max('like'))['max_likes']
    the_image.rts = tweet_query.aggregate(max_rts=Max('rt'))['max_rts']

    image_serializer = MediaSerializer(the_image, many=False)
    tweet_serializer = TweetSerializer(tweet_query, many=True)

    return Response({
        **image_serializer.data,
        "tweets": tweet_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
def setImageWeight(request, pk):
    """
    update image weight

    [url params]
    pk: image id

    [body params]
    weight: image weight
    """
    if not request.user.is_authenticated:
        return Response({"message": "Not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    if not Media.objects.filter(pk=pk).exists():
        return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract the data from the PUT request using request.data
    data = request.data

    weight = data.get('weight', None)
    if not weight:
        return Response({"message": "Weight not found"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        weight = float(weight)
    except:
        return Response({"message": "Weight has incorrect format"}, status=status.HTTP_400_BAD_REQUEST)

    # Update the fields of the object with the data from the request
    the_image = Media.objects.get(pk=pk)
    the_image.weight = weight

    # Save the updated object to the database
    the_image.save()

    return Response({"message": "Object updated successfully"}, status=status.HTTP_200_OK)


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
