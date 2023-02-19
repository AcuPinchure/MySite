from twitter_bot.models import Tweet, WeeklyStats, RtToUser, Seiyuu
from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta, datetime




class Command(BaseCommand):
    def fixFollower(self, name):
        if name == 'Kaorin':
            search = '前田佳織里'
            bot_id = 'kaorin__bot'
        elif name == 'Chemi':
            search = '田中ちえ美'
            bot_id = 'chiemi__bot'
        elif name == 'Akarin':
            search = '鬼頭明里'
            bot_id = 'akarin__bot'

        # get the start and end dates for the range
        start_date = datetime(2022, 8, 30, 2, 10, 13)
        end_date = datetime(2023, 2, 19, 3, 51, 8)

        # get the follower counts for the end and start tweets
        followers_end = Tweet.objects.filter(media__seiyuu__name=search, data_time__gt=end_date).earliest('data_time').follower
        followers_start = Tweet.objects.filter(media__seiyuu__name=search, data_time__lt=start_date).latest('data_time').follower

        # calculate the follower difference between the start and end tweets
        follower_diff = followers_end - followers_start
        tweets_missing = Tweet.objects.filter(media__seiyuu__name=search, data_time__gte=start_date, data_time__lte=end_date)
        tweet_count = tweets_missing.count()

        # calculate the increment in follower count between each tweet
        follower_increment = follower_diff / (tweet_count - 1)

        # interpolate the missing follower counts for each tweet
        current_follower = followers_start
        for tweet in tweets_missing:
            current_follower += follower_increment
            tweet.follower = int(current_follower)
            tweet.save()

            self.stdout.write(self.style.SUCCESS(f'Fixed follower for {tweet}'))
        
        # print a success message
        self.stdout.write(self.style.SUCCESS('Successfully interpolated follower field for Tweet instances'))

    def handle(self, **options):
        names = ['Kaorin','Chemi','Akarin']
        for name in names:
            self.fixFollower(name)
            