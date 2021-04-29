from django.contrib import admin
from . import models


admin.site.register(models.Feedback)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_on')
    search_fields = ['title', 'text']


admin.site.register(models.Article, ArticleAdmin)
