# Generated by Django 5.1 on 2024-11-06 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_comment_edited_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='recovery_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='two_factor_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
