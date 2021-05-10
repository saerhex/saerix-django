from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_delete, sender=models.Discussion)
def discussion_delete(sender, instance, using, **kwargs):
    print("Discussion was deleted and saved to reserve table!")
    d = models.DiscussionsDeleted()
    d.user = instance.user.id
    d.title = instance.title
    d.description = instance.description
    d.save()


@receiver(pre_save, sender=models.Discussion)
def discussion_pre_save(sender, instance, **kwargs):
    if instance.description == 'anonymous':
        print("Discussion text was empty")
        instance.description = "--author decided to leave " \
                               "description of discussion empty--"


@receiver(pre_save, sender=models.Discussion)
def discussion_pre_update(sender, instance, **kwargs):
    if not instance._state.adding:
        print("Discussion has been updated!")
        instance.description += '   updated'


@receiver(pre_delete, sender=models.Message)
def message_delete(sender, instance, using, **kwargs):
    print("Message was deleted and saved to reserve table!")
    d = models.MessagesDeleted()
    d.user = instance.user.id
    d.discussion = instance.discussion.title
    d.text = instance.text
    d.save()
