# Generated by Django 3.2 on 2023-02-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0006_auto_20230218_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklystats',
            name='delta_followers',
        ),
        migrations.AddField(
            model_name='weeklystats',
            name='follower',
            field=models.IntegerField(blank=True, help_text='Followers', null=True),
        ),
    ]
