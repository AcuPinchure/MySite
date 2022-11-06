from ._post_handler import auth_api, mediaUpload
from twitter_bot.models import Tweet,Media
import tweepy
import os
from django.utils.timezone import now
from random import choice
from django.core.management.base import BaseCommand
from pathlib import Path

def post_once(name):
    api, oauth = auth_api(name)
    if not (api and oauth):
        print("[{}] Error during authentication".format(name))
        return False
    print("[{}] Authentication OK".format(name))

    if name == 'Kaorin':
        search = '前田佳織里'
        bot_id = 'kaorin__bot'
    elif name == 'Chemi':
        search = '田中ちえ美'
        bot_id = 'chiemi__bot'
    elif name == 'Akarin':
        search = '鬼頭明里'
        bot_id = 'akarin__bot'

    media_q = Media.objects.filter(seiyuu__name=search)
    media_pks = media_q.values_list('pk', flat=True)
    random_pk = choice(media_pks)
    random_media = media_q.get(pk=random_pk)
    random_file_path = random_media.file.name.replace("\\","/")

    print("[{}] Random media: {}".format(name,random_file_path))
    
    f_path = os.path.join(Path(os.getcwd()).parent,random_file_path)
    f_type = random_media.file_type
    f_format = [f_type, 'tweet_{}'.format(f_type.split('/')[0])]
    mediaUpload(f_path, oauth, f_format)

    the_tweet = api.user_timeline(user_id=bot_id, count=1)[0]
    
    print("[{}] Posted tweet ID: {}".format(name,the_tweet.id))
    
    tweet_instance = Tweet(
        id=the_tweet.id,
        post_time=now(),
        media=random_media
    )
    tweet_instance.save()

    return True

class Command(BaseCommand):
    help = "Pick a random media and post once"
    
    def handle(self, *args, **kwargs):
        names = ['Kaorin','Chemi','Akarin']
        for name in names:
            ret = post_once(name)
            if ret:
                self.stdout.write('[{}] Post success'.format(name))
            else:
                self.stdout.write('[{}] Post failed'.format(name))