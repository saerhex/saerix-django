from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.ForumListView.as_view(), name='forum'),
    path('forum/<int:pk>', views.ForumDetailView.as_view(),
         name='forum-detail')
]
