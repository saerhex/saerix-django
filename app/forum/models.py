from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField

User = get_user_model()


class Discussion(models.Model):
    user = models.ForeignKey(User,
                             related_name='discussions',
                             on_delete=models.CASCADE,
                             db_index=True)
    title = models.CharField(max_length=200, default="anonymous")
    description = models.TextField(max_length=5000, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title[:10]


class Message(models.Model):
    user = models.ForeignKey(User,
                             related_name='messages',
                             on_delete=models.CASCADE,
                             db_index=True)
    discussion = models.ForeignKey(Discussion,
                                   related_name='messages',
                                   on_delete=models.CASCADE,
                                   db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    text = RichTextField(null=False, blank=False)

    def __str__(self):
        return f"{self.user} commented on {self.discussion.title[:10]}..."
