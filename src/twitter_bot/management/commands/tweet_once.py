from ._post_handler import auth_api, mediaUpload
from twitter_bot.models import Tweet, Media
import tweepy
import os
from django.utils.timezone import now
from random import choices
from django.core.management.base import BaseCommand
from pathlib import Path
from twitter_bot.models import Seiyuu
from datetime import timedelta


def post_once(the_seiyuu_instance: Seiyuu):
    api, oauth, client = auth_api(the_seiyuu_instance)
    if not (api and oauth and client):
        print(f"[{the_seiyuu_instance.id_name}] Error during authentication")
        return False
    print(f"[{the_seiyuu_instance.id_name}] Authentication OK")

    media_q = Media.objects.filter(seiyuu=the_seiyuu_instance)
    media_pks = media_q.values_list('pk', flat=True)
    media_weights = media_q.values_list('weight', flat=True)
    random_pk = choices(media_pks, media_weights)[0]
    random_media = media_q.get(pk=random_pk)
    random_file_path = random_media.file.name.replace("\\", "/")

    print(f"[{the_seiyuu_instance.id_name}] Random media: {random_file_path}")

    f_path = os.path.join(Path(os.getcwd()).parent, random_file_path)
    f_type = random_media.file_type
    f_format = [f_type, 'tweet_{}'.format(f_type.split('/')[0])]
    tweet_id = mediaUpload(f_path, oauth, f_format, client)

    # the_tweet = api.user_timeline(user_id=bot_id, count=1)[0]  # v1
    # the_tweet = client.get_users_tweets(id=bot_user_id, max_results=5)[0] # v2

    print(f"[{the_seiyuu_instance.id_name}] Posted tweet ID: {tweet_id}")

    tweet_instance = Tweet(
        # id=the_tweet.id, # v1
        # id=the_tweet['id'] # v2
        id=int(tweet_id),
        post_time=now(),
        media=random_media
    )
    tweet_instance.save()

    return True


class Command(BaseCommand):
    help = "For all active seiyuu, check if post interval is reach, pick a random media and post once"

    def handle(self, *args, **kwargs):
        active_seiyuu = Seiyuu.objects.filter(activated=True)

        for the_seiyuu_instance in active_seiyuu:
            curr_time = now()
            post_interval = the_seiyuu_instance.interval

            # check if last post time is older than now - interval
            if Tweet.objects.filter(media__seiyuu=the_seiyuu_instance, post_time__gt=(curr_time - timedelta(minutes=(post_interval*60-5)))).exists():
                self.stdout.write(
                    f'[{the_seiyuu_instance.id_name}] Interval not reach, pass')
                continue
            ret = post_once(the_seiyuu_instance)
            if ret:
                self.stdout.write(
                    f'[{the_seiyuu_instance.id_name}] Post success')
            else:
                self.stdout.write(
                    f'[{the_seiyuu_instance.id_name}] Post failed')
