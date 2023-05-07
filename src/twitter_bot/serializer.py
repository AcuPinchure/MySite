from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = [
            'id', 
            'post_time',
            'data_time',
            'like',
            'rt',
            'follower',
            'media'
        ]

class StatSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField() # Start date of the week
    end_date = serializers.DateTimeField() # End date of the week

    posts = serializers.IntegerField() # Total number of posts this week
    likes = serializers.IntegerField() # Total number of liks this week
    rts = serializers.IntegerField() # Total number of rts this week

    avg_likes = serializers.FloatField() # Average number of likes of all tweets this week
    avg_retweets = serializers.FloatField() # Average number of retweets of all tweets this week

    max_likes = serializers.IntegerField() # Tweet id with the highest number of likes this week
    max_rts = serializers.IntegerField() # Tweet id with the highest number of retweets this week
    
class FollowerSerializer(serializers.Serializer):
    data_time = serializers.DateTimeField() # when was this follower recorded
    followers = serializers.IntegerField() # the number of followers at that time
