# Generated by Django 3.1.7 on 2021-05-10 13:30

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20210510_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussionsDeleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=5000, null=True)),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Discussions deleted',
                'db_table': 'DiscussionsDeleted',
            },
        ),
        migrations.CreateModel(
            name='MessagesDeleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('discussion', models.CharField(max_length=200)),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
                ('text', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Messages deleted',
                'db_table': 'MessagesDeleted',
            },
        ),
    ]
