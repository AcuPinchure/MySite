from twitter_bot.models import Tweet, WeeklyStats, RtToUser, Seiyuu, Followers
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

        the_seiyuu = Seiyuu.objects.get(name=search)

        # get the start and end dates for the range
        start_date = datetime(2023, 5, 22, 7, 0, 0)
        end_date = datetime(2023, 6, 10, 21, 0, 0)

        # get the follower counts for the end and start tweets
        followers_start = Followers.objects.filter(seiyuu=the_seiyuu, data_time__lt=start_date).latest('data_time')
        followers_end = Followers.objects.filter(seiyuu=the_seiyuu, data_time__gt=end_date).earliest('data_time')

        # get missing start time
        missing_start = followers_start.data_time
        missing_end = followers_end.data_time

        #print(missing_start)
        #print(missing_end)

        #return 0

        # create missing data points without followers
        curr_time = missing_start + timedelta(hours=1)
        missing_data_points = []
        while curr_time < missing_end:
            missing_data_points.append(Followers(
                seiyuu=the_seiyuu,
                data_time=curr_time
            ))

            self.stdout.write(self.style.SUCCESS(f'Append follower data point {curr_time}'))
            curr_time += timedelta(hours=1)

        Followers.objects.bulk_create(missing_data_points)
        self.stdout.write(self.style.SUCCESS(f'Add follower data points successfully'))

        # calculate the follower difference between the start and end tweets
        followers_diff = followers_end.followers - followers_start.followers
        followers_missing = Followers.objects.filter(seiyuu=the_seiyuu, data_time__gte=start_date, data_time__lte=end_date, followers__isnull=True)
        followers_count = followers_missing.count()

        # calculate the increment in follower count between each tweet
        follower_increment = followers_diff / (followers_count - 1)

        # interpolate the missing follower counts for each tweet
        current_follower = followers_start.followers
        for follower in followers_missing:
            current_follower += follower_increment
            follower.followers = int(current_follower)

            self.stdout.write(self.style.SUCCESS(f'Append follower update for {follower}'))
        
        # print a success message
        Followers.objects.bulk_update(followers_missing, fields=["followers"])
        self.stdout.write(self.style.SUCCESS('Successfully interpolated follower field for Follower instances'))

    def handle(self, **options):
        names = ['Kaorin','Chemi','Akarin']
        for name in []:
            self.fixFollower(name)
            