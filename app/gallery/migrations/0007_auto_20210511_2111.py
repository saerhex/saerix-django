# Generated by Django 3.1.7 on 2021-05-11 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_delete_tagsdeleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentary',
            options={'verbose_name_plural': 'Commentaries'},
        ),
        migrations.RemoveField(
            model_name='commentariesdeleted',
            name='user',
        ),
        migrations.AlterField(
            model_name='commentariesdeleted',
            name='publication',
            field=models.IntegerField(),
        ),
    ]
