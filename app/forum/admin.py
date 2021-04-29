from django.contrib import admin
from . import models


admin.site.register(models.Message)


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_on')
    search_fields = ['title', 'description']


admin.site.register(models.Discussion, DiscussionAdmin)
