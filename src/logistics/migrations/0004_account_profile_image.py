# Generated by Django 3.2 on 2022-11-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0003_auto_20221121_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.FileField(blank=True, help_text='大頭貼', null=True, upload_to='avatar'),
        ),
    ]
