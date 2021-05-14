from django.urls import path
from . import views


app_name = 'gallery'
urlpatterns = [
    path('', views.GalleryListView.as_view(), name='list'),
    path('<int:pk>', views.GalleryDetailView.as_view(), name='detail'),
    path('create/', views.add_publication_view, name='create'),
    path('<int:pk>/delete',
         views.PublicationDeleteView.as_view(),
         name='delete')
]
