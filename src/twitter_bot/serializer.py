from rest_framework import serializers
from .models import Tweet, Seiyuu, Media

from datetime import timedelta


class SeiyuuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Seiyuu
        fields = [
            'id',
            'name',
            'id_name',
            'screen_name',
            'interval',
            'activated',
            'image_folder'
        ]


class MediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Media
        fields = [
            'id',
            'file',
            'file_type',
            'weight',
            'seiyuu'
        ]


class TweetSerializer(serializers.ModelSerializer):
    media_url = serializers.CharField(read_only=True, source='media.file.url')

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
            'media_url'
        ]


class StatSerializer(serializers.Serializer):

    seiyuu_id_name = serializers.CharField(required=True)  # seiyuu id_name

    start_date = serializers.DateTimeField(
        required=True)  # Start date of the week
    end_date = serializers.DateTimeField(
        required=True)  # End date of the week

    time_interval = serializers.SerializerMethodField()  # Time interval in hours

    # Total number of posts this week
    posts = serializers.IntegerField(required=True)
    # Total number of liks this week
    likes = serializers.IntegerField(required=True)
    # Total number of rts this week
    rts = serializers.IntegerField(required=True)

    # Tweet id with the highest number of likes this week
    max_likes = serializers.IntegerField(required=True)
    # Tweet id with the highest number of retweets this week
    max_rts = serializers.IntegerField(required=True)

    def get_time_interval(self, obj):
        return (obj.end_date - obj.start_date) / timedelta(hours=1)


class FollowerSerializer(serializers.Serializer):
    seiyuu_id_name = serializers.CharField(required=True)  # seiyuu id_name
    data_time = serializers.DateTimeField(
        required=True)  # when was this follower recorded
    # the number of followers at that time
    followers = serializers.IntegerField(required=True)
