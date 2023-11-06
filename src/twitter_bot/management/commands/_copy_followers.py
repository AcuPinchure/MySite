from twitter_bot.models import Tweet, Followers
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        tweet_data_with_followers = Tweet.objects.select_related('media__seiyuu')
        tweet_data_with_followers = tweet_data_with_followers.filter(follower__isnull=False)

        followers_data = []

        for data in tweet_data_with_followers:
            followers_data.append(Followers(followers=data.follower, seiyuu=data.media.seiyuu, data_time=data.data_time))
            self.stdout.write(self.style.SUCCESS("[{}]Followers data {} created".format(data.media.seiyuu, data.follower)))

        Followers.objects.bulk_create(followers_data)

        self.stdout.write(self.style.SUCCESS("Followers copy completed"))
            