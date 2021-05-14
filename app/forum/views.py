from django.contrib.auth import mixins
from django.core import exceptions
from django.contrib import messages
from django.db.models import Count, F, Max
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms


class ForumListView(generic.ListView):
    template_name = 'forum/discussions_list.html'
    context_object_name = 'discussions'
    paginate_by = 15

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        return models.Discussion.objects \
            .select_related('user') \
            .filter(title__icontains=search_query) \
            .order_by('-created_on') \
            .annotate(messages_count=Count('messages'),
                      latest_message_time=Max('messages__created_on'))


class ForumDetailView(generic.DetailView):
    template_name = 'forum/discussion_detail.html'
    context_object_name = 'discussion'
    form = forms.CreateMessage

    def get_context_data(self, **kwargs):
        context = super(ForumDetailView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_object(self):
        return models.Discussion.objects \
            .select_related('user') \
            .prefetch_related('messages') \
            .prefetch_related('messages__user') \
            .get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = forms.CreateMessage(request.POST)
            if form.is_valid():
                discussion = self.get_object()
                form.instance.user = self.request.user
                form.instance.discussion = discussion
                form.save()
                return redirect(reverse_lazy('forum:detail',
                                             kwargs={'pk': discussion.pk}))
        else:
            raise exceptions.PermissionDenied


class ForumDeleteView(mixins.LoginRequiredMixin,
                      mixins.UserPassesTestMixin,
                      generic.DeleteView):
    model = models.Discussion
    success_url = reverse_lazy('forum:list')
    template_name = 'forum/discussion_list.html'

    def get_success_url(self):
        messages.success(self.request, f'Successfully deleted '
                                       f'{self.get_object().title}')
        return self.success_url

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser


class ForumUpdateView(mixins.LoginRequiredMixin,
                      mixins.UserPassesTestMixin,
                      generic.UpdateView):
    model = models.Discussion
    template_name = 'forum/discussion_update.html'
    fields = [
        'title',
        'description'
    ]

    def get_success_url(self):
        messages.success(self.request, f'Successfully updated '
                                       f'{self.get_object().title}')
        return reverse_lazy('forum:detail',
                            kwargs={'pk': self.get_object().pk})

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser


class CreateDiscussionView(mixins.LoginRequiredMixin,
                           generic.CreateView):
    model = models.Discussion
    template_name = 'forum/discussion_create.html'
    fields = ('title',
              'description')

    def get_success_url(self, obj):
        messages.success(self.request, f'Successfully created '
                                       f'{obj.title}')
        return reverse_lazy('forum:detail',
                            kwargs={'pk': obj.pk})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(self.get_success_url(obj))
