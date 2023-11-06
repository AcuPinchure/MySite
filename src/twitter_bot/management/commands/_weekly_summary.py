from twitter_bot.models import Tweet, WeeklyStats, RtToUser, Seiyuu
from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta




class Command(BaseCommand):
    def weeklySummary(self, name):
        if name == 'Kaorin':
            search = '前田佳織里'
            bot_id = 'kaorin__bot'
        elif name == 'Chemi':
            search = '田中ちえ美'
            bot_id = 'chiemi__bot'
        elif name == 'Akarin':
            search = '鬼頭明里'
            bot_id = 'akarin__bot'

        # Get the oldest post_time in the Tweet instances
        earliest_tweet_q = Tweet.objects.filter(media__seiyuu__name=search,analyzed=False)
        if earliest_tweet_q:
            oldest_post_time = earliest_tweet_q.earliest('post_time').post_time

            # Get the oldest Sunday that is older than the oldest post_time
            oldest_sunday = oldest_post_time - timedelta(days=oldest_post_time.weekday()+1)

            # Get the newest Saturday
            newest_saturday = timezone.now() - timedelta(days=timezone.now().weekday()+2)

            # Iterate through all weeks from the oldest Sunday to the newest Saturday
            current_sunday = oldest_sunday
            while current_sunday <= newest_saturday:
                # Get the start and end dates of the current week
                current_saturday = current_sunday + timedelta(days=6)
                current_week_start = current_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
                current_week_end = current_saturday.replace(hour=23, minute=59, second=59, microsecond=999999)

                # Get the Tweet instances that fall within the current week and have not been analyzed
                tweets = Tweet.objects.filter(
                    media__seiyuu__name=search,
                    post_time__gte=current_week_start,
                    post_time__lte=current_week_end,
                    analyzed=False
                )

                # If there are any such Tweet instances, create a WeeklyStats instance for the current week
                if tweets.exists():
                    most_active_user_i = RtToUser.objects.filter(tweet__in=tweets).annotate(count=Count('user')).order_by('-count').first()
                    if most_active_user_i:
                        most_active_user = most_active_user_i.user
                    else:
                        most_active_user = None

                    stats = WeeklyStats.objects.create(
                        start_date=current_week_start.date(),
                        end_date=current_week_end.date(),

                        posts=tweets.count(),
                        likes=tweets.aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
                        rts=tweets.aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,

                        avg_likes=tweets.aggregate(avg_likes=Avg('like'))['avg_likes'] or 0,
                        avg_retweets=tweets.aggregate(avg_rts=Avg('rt'))['avg_rts'] or 0,
                        max_likes=tweets.order_by('-like').first(),
                        max_rts=tweets.order_by('-rt').first(),

                        posts_all=Tweet.objects.filter(media__seiyuu__name=search,post_time__lte=current_week_end).count(),
                        likes_all=Tweet.objects.filter(media__seiyuu__name=search,post_time__lte=current_week_end).aggregate(sum_likes=Sum('like'))['sum_likes'] or 0,
                        rts_all=Tweet.objects.filter(media__seiyuu__name=search,post_time__lte=current_week_end).aggregate(sum_rts=Sum('rt'))['sum_rts'] or 0,

                        max_likes_all=Tweet.objects.filter(media__seiyuu__name=search,post_time__lte=current_week_end).order_by('-like').first(),
                        max_rt_all=Tweet.objects.filter(media__seiyuu__name=search,post_time__lte=current_week_end).order_by('-rt').first(),
                        most_active_user=most_active_user,
                        follower=tweets.latest('post_time').follower or 0,
                        seiyuu=Seiyuu.objects.get(name=search)
                    )

                    # Set the analyzed flag for all Tweet instances that were used to create the WeeklyStats instance
                    tweets.update(analyzed=True)

                    self.stdout.write(self.style.SUCCESS(f'[{search}] Created WeeklyStats for {stats}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'[{search}] No new update before {current_week_end}'))


                # Move on to the next week
                current_sunday += timedelta(weeks=1)
        else:
            self.stdout.write(self.style.SUCCESS(f'[{search}]No new update for WeeklyStats'))


    def handle(self, **options):
        names = ['Kaorin','Chemi','Akarin']
        for name in names:
            self.weeklySummary(name)
            