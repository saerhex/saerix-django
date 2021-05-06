from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.ForumListView.as_view(), name='list'),
    path('<int:pk>', views.ForumDetailView.as_view(),
         name='detail'),
    path('<int:pk>/delete', views.ForumDeleteView.as_view(),
         name='delete'),
    path('<int:pk>/update', views.ForumUpdateView.as_view(),
         name='update'),
    path('create/', views.CreateDiscussionView.as_view(),
         name='create')
]
