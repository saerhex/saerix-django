# Generated by Django 3.1.7 on 2021-05-11 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_discussionsdeleted_messagesdeleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussionsdeleted',
            name='user',
        ),
        migrations.RemoveField(
            model_name='messagesdeleted',
            name='user',
        ),
        migrations.AlterField(
            model_name='messagesdeleted',
            name='discussion',
            field=models.IntegerField(),
        ),
    ]