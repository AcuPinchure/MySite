from ._post_handler import auth_api, mediaUpload
from twitter_bot.models import Tweet,Media
import tweepy
import os
from django.utils.timezone import now
from random import choice
from django.core.management.base import BaseCommand
from pathlib import Path

def post_once(name):
    api, oauth, client = auth_api(name)
    if not (api and oauth and client):
        print("[{}] Error during authentication".format(name))
        return False
    print("[{}] Authentication OK".format(name))

    if name == 'Kaorin':
        search = '前田佳織里'
        bot_id = 'kaorin__bot'
        bot_user_id = '1215195999552933888'
    elif name == 'Chemi':
        search = '田中ちえ美'
        bot_id = 'chiemi__bot'
        bot_user_id = '1272424253447495680'
    elif name == 'Akarin':
        search = '鬼頭明里'
        bot_id = 'akarin__bot'
        bot_user_id = '1316986331965263872'

    media_q = Media.objects.filter(seiyuu__name=search)
    media_pks = media_q.values_list('pk', flat=True)
    random_pk = choice(media_pks)
    random_media = media_q.get(pk=random_pk)
    random_file_path = random_media.file.name.replace("\\","/")

    print("[{}] Random media: {}".format(name,random_file_path))
    
    f_path = os.path.join(Path(os.getcwd()).parent,random_file_path)
    f_type = random_media.file_type
    f_format = [f_type, 'tweet_{}'.format(f_type.split('/')[0])]
    tweet_id = mediaUpload(f_path, oauth, f_format, client)

    #the_tweet = api.user_timeline(user_id=bot_id, count=1)[0]  # v1
    #the_tweet = client.get_users_tweets(id=bot_user_id, max_results=5)[0] # v2
    
    print("[{}] Posted tweet ID: {}".format(name,tweet_id))
    
    tweet_instance = Tweet(
        #id=the_tweet.id, # v1
        #id=the_tweet['id'] # v2
        id=int(tweet_id),
        post_time=now(),
        media=random_media
    )
    tweet_instance.save()

    return True

class Command(BaseCommand):
    help = "Pick a random media and post once"
    
    def handle(self, *args, **kwargs):
        #names = ['Kaorin','Chemi','Akarin']
        names = ['Chemi']
        for name in names:
            ret = post_once(name)
            if ret:
                self.stdout.write('[{}] Post success'.format(name))
            else:
                self.stdout.write('[{}] Post failed'.format(name))