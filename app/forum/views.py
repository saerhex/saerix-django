from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Max
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms


class ForumListView(generic.ListView):
    template_name = 'forum/discussions_list.html'
    context_object_name = 'discussions'

    def get_queryset(self):
        return models.Discussion.objects \
            .select_related('user') \
            .all() \
            .order_by('-created_on') \
            .annotate(messages_count=Count('messages'),
                      latest_message_time=Max('messages__created_on'))


class ForumDetailView(generic.DetailView):
    template_name = 'forum/discussion_detail.html'
    context_object_name = 'discussion'
    form = forms.CreateMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_object(self):
        return models.Discussion.objects \
            .select_related('user') \
            .prefetch_related('messages') \
            .prefetch_related('messages__user') \
            .get(pk=self.kwargs.get('pk'))

    @login_required
    def post(self, request, *args, **kwargs):
        form = forms.CreateMessage(request.POST)
        if form.is_valid():
            discussion = self.get_object()
            form.instance.user = request.user
            form.instance.discussion = discussion
            form.save()

            return redirect(reverse_lazy('forum:detail',
                                         kwargs={'pk': discussion.pk}))


class ForumUpdateView(mixins.LoginRequiredMixin,
                      mixins.UserPassesTestMixin,
                      generic.UpdateView):
    model = models.Discussion
    template_name = 'forum/discussion_update.html'
    fields = [
        'title',
        'description'
    ]

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
