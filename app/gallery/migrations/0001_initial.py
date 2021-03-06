# Generated by Django 3.1.7 on 2021-05-03 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('filesize', models.CharField(blank=True, max_length=10)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gallery.publication')),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='publications', to='gallery.Tag'),
        ),
        migrations.AddField(
            model_name='publication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to=settings.AUTH_USER_MODEL),
        ),
    ]
