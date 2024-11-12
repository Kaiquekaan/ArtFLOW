# Generated by Django 5.1 on 2024-08-29 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_achievement_post_userdata_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='userdata',
            name='profile_picture_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
