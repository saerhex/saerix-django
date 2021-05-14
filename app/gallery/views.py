from django.contrib import messages
from django.contrib.auth import mixins
from django.core import exceptions
from django.db.models import Prefetch, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
import re


class GalleryListView(generic.ListView):
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'publications'
    paginate_by = 15

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        return models.Publication.objects \
            .select_related('user') \
            .prefetch_related(Prefetch('images',
                                       queryset=models.PublicationImage.objects
                                       .all().order_by('id'))) \
            .prefetch_related('tags') \
            .filter(Q(title__icontains=search_query) |
                    Q(tags__name__iexact=search_query)) \
            .distinct()


class GalleryDetailView(generic.DetailView):
    template_name = 'gallery/gallery_detail.html'
    context_object_name = 'publication'
    form = forms.CreateCommentary

    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_object(self):
        return models.Publication.objects \
            .select_related('user') \
            .prefetch_related('images') \
            .prefetch_related('tags') \
            .prefetch_related('commentaries') \
            .prefetch_related('commentaries__user') \
            .get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = forms.CreateCommentary(request.POST)
            if form.is_valid():
                publication = self.get_object()
                form.instance.user = self.request.user
                form.instance.publication = publication
                form.save()
                return redirect(reverse_lazy('gallery:detail',
                                             kwargs={'pk': publication.pk}))
        else:
            raise exceptions.PermissionDenied


def add_publication_view(request):
    context = {}

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        tags = request.POST.get('tags')

        publication = models.Publication.objects.create(
            user=request.user,
            title=data.get('title'),
            description=data.get('description')
        )

        splited_tags = re.split(r'\s*,\s*', tags)

        for tag in splited_tags:
            try:
                obj = models.Tag.objects.get(name=tag)
            except models.Tag.DoesNotExist:
                obj = models.Tag(name=tag)
                obj.save()
            publication.tags.add(obj)

        for image in images:
            created_image = publication.images.create(image=image)

        return redirect(reverse_lazy('gallery:detail',
                                     kwargs={'pk': publication.pk}))

    return render(request, 'gallery/gallery_create.html', context)


class PublicationDeleteView(mixins.LoginRequiredMixin,
                            mixins.UserPassesTestMixin,
                            generic.DeleteView):
    model = models.Publication
    success_url = reverse_lazy('gallery:list')
    template_name = 'forum/gallery_list.html'

    def get_success_url(self):
        messages.success(self.request, f'Successfully deleted '
                                       f'{self.get_object().title}')
        return self.success_url

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser
