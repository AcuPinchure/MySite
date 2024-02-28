from rest_framework import serializers
from .models import Tweet, Seiyuu, Media, Followers

from django.db.models import Sum

from datetime import timedelta


# class ServiceConfigSerializer(serializers.Serializer):
#     seiyuu_id_name = serializers.CharField(required=True)
#     is_active = serializers.BooleanField(required=True)
#     interval = serializers.IntegerField(required=True)
#     last_post_time = serializers.DateTimeField(read_only=True)


class SeiyuuSerializer(serializers.ModelSerializer):
    last_post_time = serializers.SerializerMethodField()

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    id_name = serializers.CharField(read_only=True)
    screen_name = serializers.CharField(read_only=True)

    def get_last_post_time(self, obj):

        if Tweet.objects.filter(media__seiyuu=obj).exists():
            return Tweet.objects.filter(
                media__seiyuu=obj).latest("post_time").post_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None

    class Meta:
        model = Seiyuu
        fields = [
            'id',
            'name',
            'id_name',
            'screen_name',
            'interval',
            'activated',
            'last_post_time'
        ]


class MediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.URLField(read_only=True, source='file.url')
    file_name = serializers.SerializerMethodField()
    file_type = serializers.CharField(read_only=True)
    total_weight = serializers.SerializerMethodField()
    seiyuu_name = serializers.CharField(read_only=True, source='seiyuu.name')
    seiyuu_screen_name = serializers.CharField(
        read_only=True, source='seiyuu.screen_name')
    seiyuu_id_name = serializers.CharField(
        read_only=True, source='seiyuu.id_name')
    posts = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    rts = serializers.SerializerMethodField()

    def get_total_weight(self, obj):
        return Media.objects.filter(seiyuu=obj.seiyuu).aggregate(Sum('weight'))['weight__sum']

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]

    def get_posts(self, obj):
        return obj.tweet_set.count()

    def get_likes(self, obj):
        return obj.tweet_set.aggregate(Sum('like'))['like__sum']

    def get_rts(self, obj):
        return obj.tweet_set.aggregate(Sum('rt'))['rt__sum']

    class Meta:
        model = Media
        fields = [
            'id',
            'file',
            'file_name',
            'file_type',
            'weight',
            'total_weight',
            'seiyuu_name',
            'seiyuu_screen_name',
            'seiyuu_id_name',
            'posts',
            'likes',
            'rts'
        ]


class TweetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    media = serializers.URLField(read_only=True, source='media.file.url')

    followers = serializers.SerializerMethodField(read_only=True)

    def get_followers(self, obj):
        if not Followers.objects.filter(
                data_time__lte=obj.post_time, seiyuu=obj.media.seiyuu).exists():
            return "No data"
        return Followers.objects.filter(
            data_time__lte=obj.post_time, seiyuu=obj.media.seiyuu).latest("data_time").followers

    class Meta:
        model = Tweet
        fields = [
            'id',
            'post_time',
            'data_time',
            'like',
            'rt',
            'reply',
            'quote',
            'media',
            'followers'
        ]


# class StatSerializer(serializers.Serializer):

#     seiyuu_id_name = serializers.CharField(required=True)  # seiyuu id_name

#     start_date = serializers.DateTimeField(
#         required=True)  # Start date of the week
#     end_date = serializers.DateTimeField(
#         required=True)  # End date of the week

#     time_interval = serializers.SerializerMethodField()  # Time interval in hours

#     # Total number of posts this week
#     posts = serializers.IntegerField(required=True)
#     # Total number of liks this week
#     likes = serializers.IntegerField(required=True)
#     # Total number of rts this week
#     rts = serializers.IntegerField(required=True)

#     # Tweet id with the highest number of likes this week
#     max_likes = serializers.IntegerField(required=True)
#     # Tweet id with the highest number of retweets this week
#     max_rts = serializers.IntegerField(required=True)

#     def get_time_interval(self, obj):
#         return (obj.end_date - obj.start_date) / timedelta(hours=1)


# class FollowerSerializer(serializers.Serializer):
#     seiyuu_id_name = serializers.CharField(required=True)  # seiyuu id_name
#     data_time = serializers.DateTimeField(
#         required=True)  # when was this follower recorded
#     # the number of followers at that time
#     followers = serializers.IntegerField(required=True)
