import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),
               path('admin/', admin.site.urls),
               path('', include('accounts.urls')),
               path('', include('gallery.urls')),
               path('', include('articles.urls')),
               path('', include('forum.urls'))
               ] + static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
