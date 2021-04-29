from django.db.models import Count, F
from django.db.models.functions import Greatest
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models
from . import forms


class ForumListView(generic.ListView):
    template_name = 'forum/discussions_list.html'
    context_object_name = 'discussions'

    def get_queryset(self):
        return models.Discussion.objects \
            .select_related('user') \
            .annotate(messages_count=Count('messages'),
                      latest_msg_time=Greatest('messages__created_on',
                                               None)) \
            .all() \
            .order_by('-created_on')


class ForumDetailView(generic.DetailView):
    template_name = 'forum/discussion_detail.html'
    context_object_name = 'discussion'

    def get_queryset(self):
        return models.Discussion.objects \
            .select_related('user') \
            .all()

    def get_object(self):
        return self.get_queryset() \
            .prefetch_related('messages') \
            .prefetch_related('messages__user') \
            .get(pk=self.kwargs.get('pk'))
