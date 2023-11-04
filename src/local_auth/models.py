from django.db import models
from django.contrib.auth.models import User
import uuid
from rest_framework.authtoken.models import Token

# Create your models here.

class UserExtend(models.Model):
    class Meta:
        db_table = 'auth_userextend'
    def __str__(self):
        return "UserExtend: {} of {}".format(self.nickname, self.user.username)
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(help_text='User nickname', max_length=20,blank=True,null=True)
    
    app = models.ForeignKey('App',on_delete=models.CASCADE,help_text='App which the user belongs to')
    user = models.ForeignKey(User,on_delete=models.CASCADE,help_text='User')

class App(models.Model):
    class Meta:
        db_table = 'auth_app'
    def __str__(self):
        return "APP: {}".format(self.name)
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(help_text='App name', max_length=50,blank=True,null=True)
    router = models.CharField(help_text='App URL router', max_length=50,blank=True,null=True)
    auth_required = models.BooleanField(help_text='Whether authentication is required', default=False)

