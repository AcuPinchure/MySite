# Generated by Django 3.2 on 2022-09-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='protected',
            field=models.BooleanField(blank=True, help_text='If the account is private', null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='verified',
            field=models.BooleanField(blank=True, help_text='If the account has the blue check mark', null=True),
        ),
    ]
