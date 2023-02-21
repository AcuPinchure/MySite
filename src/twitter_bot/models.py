from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

class Seiyuu(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_seiyuu'

    name = models.CharField(help_text='Seiyuu Name', max_length=20,blank=False)
    screen_name = models.CharField(help_text='Bot account screen name', max_length=20,blank=True,null=True)
    id_name = models.CharField(help_text='Seiyuu short name', max_length=20,blank=True,null=True)
    

    def __str__(self):
        return self.name

# Seiyuu.objects = Seiyuu.objects.using('bot_data')

#########################################

# media, image or video
class Media(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_media'

    id = models.BigAutoField(primary_key=True)
    file = models.FileField(storage=FileSystemStorage(location='/.images'),help_text='Image or Video file',blank=False)
    file_type = models.CharField(
        max_length=20,
        help_text='The file type',
        choices=[
            ('image/jpg','JPG'),
            ('image/png','PNG'),
            ('video/mp4','MP4'),
            ('gif/gif','GIF')
        ],
        default='image/jpg')
    
    weight = models.FloatField(help_text="Weight for random choice",default=1.0)
    
    seiyuu = models.ForeignKey(Seiyuu,on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}".format(self.seiyuu.name, self.id)

# Media.objects = Media.objects.using('bot_media')

#########################################

# who interacted with bot
class UserAccount(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_useraccount'

    id = models.IntegerField(
        help_text='The UID of user object in twitter API',
        primary_key=True)
    name = models.CharField(help_text='Display name',max_length=255,blank=True)
    screen_name = models.CharField(help_text='ID name (with @ sign)',max_length=255,blank=True)
    location = models.CharField(help_text='The location in their profile',max_length=255,blank=True)
    protected = models.BooleanField(help_text='If the account is private',blank=True,null=True)
    verified = models.BooleanField(help_text='If the account has the blue check mark',blank=True,null=True)
    followers = models.IntegerField(help_text='The # of followers (fans)',blank=True,null=True)
    followings = models.IntegerField(help_text='The # of followings',blank=True,null=True)

# UserAccount.objects = UserAccount.objects.using('bot_data')

########################################


class Tweet(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_tweet'

    id = models.IntegerField(help_text='Tweet ID',primary_key=True)
    post_time = models.DateTimeField(help_text='Tweet time',blank=True,null=True)
    data_time = models.DateTimeField(help_text='Data collected time',blank=True,null=True)
    like = models.SmallIntegerField(help_text='Likes',blank=True,null=True)
    like_user = models.ManyToManyField(
        UserAccount,through='LikeToUser',
        help_text='The user list that likes this tweet',
        related_name='likes',blank=True)
    rt = models.SmallIntegerField(help_text='Retweets',blank=True,null=True)
    rt_user = models.ManyToManyField(
        UserAccount,through='RtToUser',
        help_text='The user list that RT this tweet',
        related_name='rts',blank=True)
    rt_spread = models.SmallIntegerField(help_text='Sum of followers of all RTing users',blank=True,null=True)
    follower = models.SmallIntegerField(help_text='Followers',blank=True,null=True)

    media = models.ForeignKey(Media,on_delete=models.PROTECT)

    analyzed = models.BooleanField(help_text='Whether the tweet has been analyzed', default=False)

    def __str__(self):
        return "[{}]-{}-{}".format(self.media.seiyuu.name,self.post_time, self.id)

# Tweet.objects = Tweet.objects.using('bot_data')

#########################################

class LikeToUser(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_liketouser'

    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return "Tweet: {}, Liked user: {}".format(self.tweet.id,self.user.id)

# LikeToUser.objects = LikeToUser.objects.using('bot_data')

#########################################

class RtToUser(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_rttouser'

    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return "Tweet: {}, RT user: {}".format(self.tweet.id,self.user.id)

# RtToUser.objects = RtToUser.objects.using('bot_data')


# stats
class WeeklyStats(models.Model):
    class Meta:
        # managed = False
        db_table = 'weekly_stats'

    start_date = models.DateField(help_text='Start date of the week', blank=True, null=True)
    end_date = models.DateField(help_text='End date of the week', blank=True, null=True)

    posts = models.PositiveIntegerField(help_text='Total number of posts this week', blank=True, null=True)
    likes = models.PositiveIntegerField(help_text='Total number of liks this week', blank=True, null=True)
    rts = models.PositiveIntegerField(help_text='Total number of rts this week', blank=True, null=True)

    avg_likes = models.FloatField(help_text='Average number of likes of all tweets this week', blank=True, null=True)
    avg_retweets = models.FloatField(help_text='Average number of retweets of all tweets this week', blank=True, null=True)

    max_likes = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='max_likes_stats',
        help_text='Tweet instance with the highest number of likes this week', blank=True, null=True)
    max_rts = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='max_rt_stats',
        help_text='Tweet instance with the highest number of retweets this week', blank=True, null=True)

    posts_all = models.PositiveIntegerField(help_text='Total number of posts of all time', blank=True, null=True)
    likes_all = models.PositiveIntegerField(help_text='Total number of liks of all time', blank=True, null=True)
    rts_all = models.PositiveIntegerField(help_text='Total number of rts of all time', blank=True, null=True)

    max_likes_all = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='max_likes_stats_all',
        help_text='Tweet instance with the highest number of likes of all time', blank=True, null=True)
    max_rt_all = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='max_rt_stats_all',
        help_text='Tweet instance with the highest number of retweets of all time', blank=True, null=True)

    most_active_user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='weekly_stats',
        help_text='The most active user this week, who appears most frequently in the field rt_user of all tweets', blank=True, null=True)
    follower = models.IntegerField(help_text='Followers', blank=True, null=True)

    seiyuu = models.ForeignKey(Seiyuu,on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return f"WeeklyStats from {self.start_date} to {self.end_date}"