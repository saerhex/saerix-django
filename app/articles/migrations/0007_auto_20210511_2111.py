# Generated by Django 3.1.7 on 2021-05-11 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20210510_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlesdeleted',
            name='user',
        ),
        migrations.RemoveField(
            model_name='feedbacksdeleted',
            name='user',
        ),
    ]
