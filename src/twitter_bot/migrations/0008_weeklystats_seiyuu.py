# Generated by Django 3.2 on 2023-02-18 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0007_auto_20230218_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklystats',
            name='seiyuu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='twitter_bot.seiyuu'),
        ),
    ]