from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import (render, redirect, get_object_or_404)
from . import models
from . import forms


class ArticleList(generic.ListView):
    context_object_name = 'articles'
    queryset = models.Article.objects \
        .select_related('user') \
        .all() \
        .order_by('-created_on')
    template_name = 'articles/articles.html'
    paginate_by = 15


def article_detail_view(request, pk):
    context = {}
    article = models.Article.objects \
        .select_related('user') \
        .annotate(likes=Count('feedbacks', filter=Q(feedbacks__mark=1)),
                  dislikes=Count('feedbacks', filter=Q(feedbacks__mark=0))) \
        .get(pk=pk)
    context['article'] = article
    if request.user.is_authenticated:
        try:
            feedback = models.Feedback.objects \
                .get(user=request.user,
                     article=article)
            context['vote'] = feedback
        except models.Feedback.DoesNotExist:
            pass
    return render(request, 'articles/articles_detail.html', context=context)


VOTES = {
    'like': 1,
    'dislike': 0
}


@login_required
def add_vote(request, pk, vote):
    mark = VOTES.get(vote)
    user = request.user
    article = models.Article.objects.get(pk=pk)
    try:
        vote = models.Feedback.objects \
            .get(user=user,
                 article=article)
        if vote.mark == mark:
            vote.delete()
        else:
            vote.mark = mark
            vote.save()
    except models.Feedback.DoesNotExist:
        vote = models.Feedback.objects \
            .create(user=user, article=article,
                    mark=mark)
        vote.save()
    return redirect(reverse_lazy('articles:detail', kwargs={'pk': pk}))


@login_required
def add_article_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        title = request.POST.get('title')
        user = request.user
        data = {'user': user,
                'text': text,
                'title': title}
        form = forms.AddArticleForm(data)
        if form.is_valid():
            article = form.save()
            article.save()
            messages.success(request, 'Created article successfully!')
            return redirect(reverse_lazy('articles:detail',
                                         kwargs={'pk': article.pk}))
    else:
        form = forms.AddArticleForm()

    return render(request, 'articles/add_article.html', {'form': form})


@login_required
def delete_article_view(request, pk):
    user = request.user
    article = get_object_or_404(models.Article, pk=pk)
    if article.user == user or user.is_superuser:
        article.delete()
        messages.success(request, 'Deleted article successfully!')
        return redirect(reverse_lazy('articles:list'))
    else:
        messages.error(request, 'You don\'t have permission '
                                'to delete this article!')
        return redirect(reverse_lazy('gallery:list'))


@login_required
def update_article_view(request, pk):
    user = request.user
    article = models.Article.objects \
        .select_related('user') \
        .get(pk=pk)
    context = {}
    if article.user == user or user.is_superuser:
        if request.method == 'POST':
            form = forms.UpdateArticleForm(request.POST)
            if form.is_valid():
                new_title = form.cleaned_data.get('title')
                new_text = form.cleaned_data.get('text')
                article.title = new_title
                article.text = new_text
                article.save()
                messages.success(request, 'Updated article successfully')
                return redirect(reverse_lazy('articles:list'))
            else:
                context['article'] = article
        return render(request, 'articles/update_article.html', context=context)
    else:
        messages.error(request, 'You don\'t have permission '
                                'to update this article!')
        return redirect(reverse_lazy('gallery:list'))


def lab_22_discussions_view(request):
    c = connection.cursor()
    r = ''
    if request.method == 'POST':
        form = forms.FirstTaskForm(request.POST)
        if form.is_valid():
            try:
                year = form.cleaned_data.get('date')
                c.callproc('get_discussions_later', (2019,))
                r = c.fetchall()
                return render(request, 'lab22/first.html', {'result': r})
            finally:
                c.close()
    else:
        form = forms.FirstTaskForm()
    return render(request, 'lab22/first.html', {'result': r, 'form': form})


def lab_22_articles_view(request):
    c = connection.cursor()
    r = ''
    if request.method == 'POST':
        form = forms.FirstTaskForm(request.POST)
        if form.is_valid():
            try:
                year = form.cleaned_data.get('date')
                c.callproc('get_articles', (year,))
                r = c.fetchall()
                return render(request, 'lab22/second.html', {'result': r})
            finally:
                c.close()
    else:
        form = forms.FirstTaskForm()
    return render(request, 'lab22/second.html', {'result': r, 'form': form})
