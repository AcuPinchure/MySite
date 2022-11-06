import os
from pathlib import Path
from twitter_bot.models import Media, Seiyuu
from django.core.management.base import BaseCommand

#c = Seiyuu.objects.create(name='田中ちえ美')
#c.save()

class Command(BaseCommand):
    def handle(self, **options):

        for info in [
            ('前田佳織里','KaorinPicture'),
            ('鬼頭明里','AkarinPicture'),
            ('田中ちえ美','ChemiPicture')
        ]:

            name, id = info
            
            s = Seiyuu.objects.get(name=name)

            root_path = Path(__file__).resolve().parent.parent.parent.parent.parent

            imgs_path = os.path.join(root_path,'data','media','Library',id)
            imgs = os.listdir(imgs_path)

            for idx, img in enumerate(imgs):
                file_type = ""
                if img.lower().endswith(".jpg"):
                    file_type = 'image/jpg'
                elif img.lower().endswith(".png"):
                    file_type = 'image/png'
                elif img.lower().endswith(".mp4"):
                    file_type = 'video/mp4'
                elif img.lower().endswith(".gif"):
                    file_type = 'gif/gif'
                else:
                    raise ValueError("Invalid file_type: {}".format(img.split(".")[-1].lower()))
                i = Media.objects.create(
                    file=os.path.join('data','media','Library',id,img),
                    seiyuu=s,
                    file_type = file_type)
                i.save()
                print("Now at: {}-{}".format(idx, img))
        