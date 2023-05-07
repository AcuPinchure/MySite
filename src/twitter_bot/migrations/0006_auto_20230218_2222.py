# Generated by Django 3.2 on 2023-02-18 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0005_auto_20230218_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklystats',
            name='avg_likes',
            field=models.FloatField(blank=True, help_text='Average number of likes of all tweets this week', null=True),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='avg_retweets',
            field=models.FloatField(blank=True, help_text='Average number of retweets of all tweets this week', null=True),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='delta_followers',
            field=models.IntegerField(blank=True, help_text='Delta of followers compared to last week', null=True),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='end_date',
            field=models.DateField(blank=True, help_text='End date of the week', null=True),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='max_likes',
            field=models.ForeignKey(blank=True, help_text='Tweet instance with the highest number of likes this week', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='max_likes_stats', to='twitter_bot.tweet'),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='max_likes_all',
            field=models.ForeignKey(blank=True, help_text='Tweet instance with the highest number of likes of all time', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='max_likes_stats_all', to='twitter_bot.tweet'),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='max_rt_all',
            field=models.ForeignKey(blank=True, help_text='Tweet instance with the highest number of retweets of all time', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='max_rt_stats_all', to='twitter_bot.tweet'),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='max_rts',
            field=models.ForeignKey(blank=True, help_text='Tweet instance with the highest number of retweets this week', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='max_rt_stats', to='twitter_bot.tweet'),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='most_active_user',
            field=models.ForeignKey(blank=True, help_text='The most active user this week, who appears most frequently in the field rt_user of all tweets', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekly_stats', to='twitter_bot.useraccount'),
        ),
        migrations.AlterField(
            model_name='weeklystats',
            name='start_date',
            field=models.DateField(blank=True, help_text='Start date of the week', null=True),
        ),
    ]