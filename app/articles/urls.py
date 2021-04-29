from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='articles'),
    path('articles/add', views.add_article_view, name='add-article'),
    path('articles/<int:pk>', views.article_detail_view,
         name='articles-detail'),
    path('articles/<int:pk>/delete', views.delete_article_view,
         name='delete-article'),
    path('articles/<int:pk>/update', views.update_article_view,
         name='update-article'),
    path('articles/<int:pk>/<str:vote>', views.add_vote, name='vote'),
]
