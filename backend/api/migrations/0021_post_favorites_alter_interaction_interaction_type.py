# Generated by Django 5.1 on 2024-09-23 21:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_interaction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='interaction_type',
            field=models.CharField(choices=[('view', 'View'), ('like', 'Like'), ('comment', 'Comment'), ('favorite', 'Favorite')], max_length=20),
        ),
    ]
