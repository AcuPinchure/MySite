from django.contrib import admin
from .models import Seiyuu, Media, Tweet, UserAccount, LikeToUser, RtToUser, WeeklyStats

# Register your models here.

admin.site.register(Seiyuu)
admin.site.register(Media)
admin.site.register(Tweet)
admin.site.register(UserAccount)
admin.site.register(LikeToUser)
admin.site.register(RtToUser)
admin.site.register(WeeklyStats)