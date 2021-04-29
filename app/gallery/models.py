from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Publications(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
