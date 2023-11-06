import tweepy
import os
import sys
import time
# print(tweepy.__version__) #3.8
import json
import requests
from requests_oauthlib import OAuth1
from pathlib import Path

from twitter_bot.models import Seiyuu


# The media upload method
MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'


class MediaTweet(object):

    def __init__(self, file_name, auth, client):
        '''
        Defines video tweet properties
        '''
        self.video_filename = file_name
        self.total_bytes = os.path.getsize(self.video_filename)
        self.media_id = None
        self.processing_info = None
        self.auth = auth
        self.client = client

    def upload_init(self, form):  # form: ['image/jpg','tweet_image']
        '''
        Initializes Upload
        '''
        print('INIT')

# the file format

        request_data = {
            'command': 'INIT',
            'media_type': form[0],
            'total_bytes': self.total_bytes,
            'media_category': form[1]
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL,
                            data=request_data, auth=self.auth)
        media_id = req.json()['media_id']

        self.media_id = media_id

        # print('Media ID: %s' % str(media_id))

    def upload_append(self):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        segment_id = 0
        bytes_sent = 0
        file = open(self.video_filename, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)

            print('APPEND')

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media': chunk
            }

            req = requests.post(url=MEDIA_ENDPOINT_URL,
                                data=request_data, files=files, auth=self.auth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('%s of %s bytes uploaded' %
                  (str(bytes_sent), str(self.total_bytes)))

        # print('Upload chunks complete.')

    def upload_finalize(self):
        '''
        Finalizes uploads and starts video processing
        '''
        # print('FINALIZE')

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL,
                            data=request_data, auth=self.auth)
        print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        '''
        Checks video processing status
        '''
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        # print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=MEDIA_ENDPOINT_URL,
                           params=request_params, auth=self.auth)

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

# post message
    def tweet(self):
        '''
        Publishes Tweet with attached video
        '''
        request_data = {
            'status': '',
            'media_ids': self.media_id
        }

        req = requests.post(url=POST_TWEET_URL,
                            data=request_data, auth=self.auth)
        # print(req.json())

    def tweet_v2(self):
        req = self.client.create_tweet(
            media_ids=[self.media_id], user_auth=True)
        print(req)
        return req.data['id']


def mediaUpload(FILENAME, auth, form, client):
    mediaTweet = MediaTweet(FILENAME, auth, client)
    mediaTweet.upload_init(form)
    mediaTweet.upload_append()
    mediaTweet.upload_finalize()
    tweet_id = mediaTweet.tweet_v2()
    return tweet_id


def getForm(ftype):
    ftype = ftype.lower()
    if ftype == 'jpg' or ftype == 'jpeg':
        form = ['image/jpg', 'tweet_image']
    elif ftype == 'png':
        form = ['image/png', 'tweet_image']
    elif ftype == 'gif':
        form = ['gif/gif', 'tweet_gif']
    elif ftype == 'mp4':
        form = ['video/mp4', 'tweet_video']
    else:
        raise ValueError('no such file type: {}'.format(ftype))
    return form

# main post action is here


root_path = Path(__file__).resolve().parent.parent.parent.parent.parent
with open(os.path.join(root_path, "data", "tokens.json"), "r", encoding="UTF-8") as token_j:
    tokens = json.load(token_j)

with open(os.path.join(root_path, "data", "tokens_v2.json"), "r", encoding="UTF-8") as token_v2_j:
    tokens_v2 = json.load(token_v2_j)


def auth_api(the_seiyuu_instance: Seiyuu):
    try:
        the_token = tokens[the_seiyuu_instance.id_name]
        the_token_v2 = tokens_v2[the_seiyuu_instance.id_name]
    except KeyError:
        raise ValueError(
            f'Token missing for id_name: {the_seiyuu_instance.id_name}')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(the_token["id"], the_token["id_secret"])
    auth.set_access_token(the_token["access"], the_token["access_secret"])
    oauth = OAuth1(the_token["id"], the_token["id_secret"],
                   the_token["access"], the_token["access_secret"])

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        client = tweepy.Client(
            bearer_token=the_token_v2['bearer_token'],
            consumer_key=the_token["id"],
            consumer_secret=the_token["id_secret"],
            access_token=the_token["access"],
            access_token_secret=the_token["access_secret"],
        )
    except tweepy.errors.Unauthorized:
        # print("Error during authentication")
        return None, None, None
    else:
        # print("Authentication OK")
        return api, oauth, client


def auth_api_v2():
    client = tweepy.Client(
        bearer_token=tokens_v2["AcuPinchure"]["bearer_token"])

    return client


if __name__ == '__main__':
    pass
