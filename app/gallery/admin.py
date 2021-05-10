from django.contrib import admin
from . import models


admin.site.register(models.Tag)
admin.site.register(models.Publication)
admin.site.register(models.PublicationImage)
admin.site.register(models.Commentary)
admin.site.register(models.CommentariesDeleted)
