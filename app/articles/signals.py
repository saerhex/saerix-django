from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_delete, sender=models.Article)
def article_delete(sender, instance, using, **kwargs):
    print("Article saved to reserve table!")
    d = models.ArticlesDeleted()
    d.title = instance.title
    d.text = instance.text
    d.save()


@receiver(pre_save, sender=models.Article)
def article_pre_save(sender, instance, **kwargs):
    if instance.text == 'anon':
        print("Article text was empty")
        instance.text = "--author decided to leave this field empty--"


@receiver(pre_save, sender=models.Article)
def article_pre_update(sender, instance, **kwargs):
    if not instance._state.adding:
        print("Articles updated!")
        instance.text += 'updated'


@receiver(pre_delete, sender=models.Feedback)
def feedback_delete(sender, instance, using, **kwargs):
    print("Feedbacks deleted and saved to reserve table!")
    d = models.FeedbacksDeleted()
    d.article = instance.article.id
    d.mark = instance.mark
    d.save()
