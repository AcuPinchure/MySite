# Generated by Django 3.2 on 2023-07-30 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0012_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followers',
            name='data_time',
            field=models.DateTimeField(blank=True, help_text='Data collected time', null=True),
        ),
    ]
