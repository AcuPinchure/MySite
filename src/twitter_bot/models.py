from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

class Seiyuu(models.Model):
    class Meta:
        # managed = False
        db_table = 'bot_seiyuu'

    name = models.CharField(help_text='Seiyuu Name', max_length=20,blank=False)
        
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