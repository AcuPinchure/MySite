# Generated by Django 3.2 on 2022-11-21 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-create_time', 'name']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-create_time']},
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(blank=True, help_text='Which user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
