from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.ArticleList.as_view(),
         name='list'),
    path('create', views.add_article_view,
         name='create'),
    path('<int:pk>', views.article_detail_view,
         name='detail'),
    path('<int:pk>/delete', views.delete_article_view,
         name='delete'),
    path('<int:pk>/update', views.update_article_view,
         name='update'),
    path('<int:pk>/<str:vote>', views.add_vote,
         name='vote'),
    path('lab22/first', views.lab_22_discussions_view, name='first_task'),
    path('lab22/second', views.lab_22_articles_view, name='second_task')
]
