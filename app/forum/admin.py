from django.contrib import admin
from . import models


admin.site.register(models.Message)
admin.site.register(models.MessagesDeleted)
admin.site.register(models.DiscussionsDeleted)


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_on')
    search_fields = ['title', 'description']


admin.site.register(models.Discussion, DiscussionAdmin)
