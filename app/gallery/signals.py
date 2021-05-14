from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from . import models
from hurry.filesize import size as convert_size
from hurry.filesize import verbose


@receiver(pre_delete, sender=models.Commentary)
def commentary_delete(sender, instance, using, **kwargs):
    print("Commentary was deleted and saved to reserve table!")
    d = models.CommentariesDeleted()
    d.publication = instance.publication.id
    d.text = instance.text
    d.save()


@receiver(pre_save, sender=models.PublicationImage)
def image_save(sender, instance, **kwargs):
    filesize = convert_size(instance.image.size, system=verbose)
    instance.filesize = filesize
