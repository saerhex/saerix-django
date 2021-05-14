from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


MARK = (
    (0, "Dislike"),
    (1, "Like"),
)

MARKS = {
    0: 'Dislike',
    1: 'Like',
}


class Article(models.Model):
    user = models.ForeignKey(User,
                             related_name='articles',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Articles'
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Feedback(models.Model):
    user = models.ForeignKey(User,
                             related_name='feedbacks',
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='feedbacks',
                                on_delete=models.CASCADE)
    mark = models.IntegerField(choices=MARK, default=1)

    class Meta:
        db_table = 'Feedbacks'

    def __str__(self):
        return f"{self.user} {MARKS.get(self.mark)} on" \
               f" {self.article.title[:10]}"


class ArticlesDeleted(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    deleted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Articles deleted'
        db_table = 'ArticlesDeleted'


class FeedbacksDeleted(models.Model):
    article = models.IntegerField()
    mark = models.IntegerField(choices=MARK, default=1)

    class Meta:
        verbose_name_plural = 'Feedbacks deleted'
        db_table = 'FeedbacksDeleted'
