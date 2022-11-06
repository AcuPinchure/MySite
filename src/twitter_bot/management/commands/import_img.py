import os
from pathlib import Path
from twitter_bot.models import Media, Seiyuu
from django.core.management.base import BaseCommand


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
            import_path = os.path.join(root_path,'data','media','ImportQueue',id)
            
            imgs = os.listdir(imgs_path)
            import_imgs = os.listdir(import_path)

            import_len = len(import_imgs)

            for idx, img in enumerate(import_imgs):
                ret = 'Failed'
                if not (img in imgs):
                    os.rename(
                        os.path.join(import_path,img),
                        os.path.join(imgs_path,img)
                    )
                    if img.lower().endswith(".jpg") or img.lower().endswith(".jpeg"):
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
                    ret = 'Success'
                    
                print("Now at: {}/{} - {} - {}".format(idx+1, import_len, img, ret))
            