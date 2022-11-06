import os
from pathlib import Path
from twitter_bot.models import Media
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        for file_type, end_with in [
            #('image/jpg','.jpg'),
            #('image/jpg','.jpeg'),
            ('image/png','.png'),
            ('video/mp4','.mp4'),
            ('gif/gif','.gif')
        ]:

            q = Media.objects.filter(file__iendswith=end_with)

            for the_media in q:
                id = the_media.id
                file = the_media.file.name
                the_media.file_type = file_type
                the_media.save()
                print("Media: {} - {} - Success".format(id,file))
            