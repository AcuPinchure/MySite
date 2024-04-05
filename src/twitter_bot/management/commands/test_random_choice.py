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


class Command(BaseCommand):
    help = "For all active seiyuu, check if post interval is reach, pick a random media and post once"

    def handle(self, *args, **kwargs):
        the_seiyuu_instance = Seiyuu.objects.get(id_name="kaorin")
        media_q = Media.objects.filter(seiyuu=the_seiyuu_instance)
        media_pks = media_q.values_list('pk', flat=True)
        media_weights = media_q.values_list('weight', flat=True)

        for i in range(100):
            random_pk = choices(media_pks, media_weights)[0]
            random_media = media_q.get(pk=random_pk)
            random_file_path = random_media.file.name.replace("\\", "/")

            print(
                f"[{the_seiyuu_instance.id_name}] Random media: {random_file_path}")
