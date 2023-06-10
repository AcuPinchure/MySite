from ._post_handler import auth_api_v2
from twitter_bot.models import Tweet,UserAccount
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from datetime import timedelta


def data_once(name):
    client = auth_api_v2()

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

    # get tweet q with no data time and
    # more than 24 hours ago
    time_buffer = 24 # hours

    #load followers
    the_user_data = client.get_user(id=bot_user_id, user_fields="public_metrics")


    tweet_q = Tweet.objects.filter(
        data_time__isnull=True,
        media__seiyuu__name=search,
        post_time__lte=now()-timedelta(hours=time_buffer)
    )
    for tweet in tweet_q:
        tweet_id = tweet.id
        print('[{}] Collecting data: {}'.format(name,tweet_id))
        tweet_data = client.get_tweet(id=str(tweet_id),tweet_fields="public_metrics")
        tweet.like = tweet_data.data.public_metrics["like_count"]
        tweet.rt = tweet_data.data.public_metrics["retweet_count"]
        tweet.reply = tweet_data.data.public_metrics["reply_count"]
        tweet.quote = tweet_data.data.public_metrics["quote_count"]
        tweet.follower = the_user_data.data.public_metrics["followers_count"]
        tweet.list_count = the_user_data.data.public_metrics["listed_count"]

        # disable rter tracking to avoid over usage
        """
        spread_count = 0

        # get rt user info
        for rt in api.get_retweets(tweet_id):
            rt_user = rt.user

            if rt_user.location:
                location = rt_user.location
            else:
                location = '(Not specified)'

            if UserAccount.objects.filter(pk=rt_user.id).exists():
                the_user = UserAccount.objects.get(pk=rt_user.id)
            else:
                the_user = UserAccount.objects.create(pk=rt_user.id)

            the_user.id=rt_user.id
            the_user.name=rt_user.name
            the_user.screen_name = rt_user.screen_name
            the_user.location = location
            the_user.protected = rt_user.protected
            the_user.verified = rt_user.verified

            the_user.followers = rt_user.followers_count
            spread_count += rt_user.followers_count

            the_user.followings = rt_user.friends_count
            
            tweet.rt_user.add(the_user)

            the_user.save()
        

        tweet.rt_spread=spread_count
        """


        tweet.data_time = now()

        tweet.save()

    return True

    

class Command(BaseCommand):
    help = "Pick a random media and post once"
    
    def handle(self, *args, **kwargs):
        names = ['Kaorin','Chemi','Akarin']
        for name in names:
            ret = data_once(name)
            if ret:
                self.stdout.write('[{}] Data collecting success'.format(name))
            else:
                self.stdout.write('[{}] Data collecting failed'.format(name))