import os
from pathlib import Path
from twitter_bot.models import Media, Tweet
from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime, timedelta



class Command(BaseCommand):
    def handle(self, **options):

        root_path = Path(__file__).resolve().parent.parent.parent.parent.parent
        worksheet = os.path.join(root_path,'data','worksheet')

        for info in [
            #('botLogKaorin','KaorinPicture', '前田佳織里'),
            ('botLogAkarin','AkarinPicture', '鬼頭明里'),
            ('botLogChiemi','ChemiPicture', '田中ちえ美')
        ]:
            path, img_path, name = info

            df = pd.read_excel(os.path.join(worksheet,f'{path} archive.xlsx'))
            df = df.fillna('')
            # print(len(df))
            for idx in range(len(df)):
                row = df.iloc[idx]
                pic = row['picName']
                tweet_id = ""
                if row['id']:
                    tweet_id = row['id'].split('id_')[1]
                post_time = datetime.strftime(row['time'],'%Y-%m-%d %H:%M:%S')
                # print(tweet_id)
                if tweet_id and (pic in os.listdir(os.path.join(root_path,'data','media','Library',img_path))) and Tweet.objects.filter(id=tweet_id).exists():
                    t = Tweet.objects.get(id=int(tweet_id))
                    t.data_time = t.post_time - timedelta(hours=24)
                    
                    
                    t.save()
                    print("[{}-{}] Tweet {} created".format(name,idx,tweet_id))
                else:
                    print("[{}-{}] Img {} doesn't exist".format(name,idx,pic))

                
