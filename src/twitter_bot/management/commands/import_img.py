import os
from pathlib import Path
from twitter_bot.models import Media, Seiyuu
from django.core.management.base import BaseCommand
from MySite.settings import BASE_DIR


class Command(BaseCommand):
    help = "Import new image from ImportQueue to Library, and create Media instance"

    def handle(self, **options):

        for the_seiyuu_instance in Seiyuu.objects.all():

            imgs_path = os.path.join(
                BASE_DIR, 'data', 'media', 'Library', the_seiyuu_instance.image_folder)
            import_path = os.path.join(
                BASE_DIR, 'data', 'media', 'ImportQueue', the_seiyuu_instance.image_folder)

            imgs = os.listdir(imgs_path)
            import_imgs = os.listdir(import_path)

            import_len = len(import_imgs)

            for idx, img in enumerate(import_imgs):
                ret = 'Failed'
                if not (img in imgs):
                    os.rename(
                        os.path.join(import_path, img),
                        os.path.join(imgs_path, img)
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
                        raise ValueError("Invalid file_type: {}".format(
                            img.split(".")[-1].lower()))
                    i = Media.objects.create(
                        file=os.path.join(
                            'data', 'media', 'Library', the_seiyuu_instance.image_folder, img),
                        seiyuu=the_seiyuu_instance,
                        file_type=file_type)
                    i.save()
                    ret = 'Success'

                self.stdout.write(self.style.SUCCESS(
                    f"[{the_seiyuu_instance.id_name}] Now at: {idx+1}/{import_len} - {img} - {ret}"))
