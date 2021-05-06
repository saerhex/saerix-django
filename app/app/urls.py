import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy

urlpatterns = [
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('admin/', admin.site.urls),
                  path('', lambda req: redirect(reverse_lazy('gallery:list'))),
                  path('', include('accounts.urls')),
                  path('gallery/', include('gallery.urls')),
                  path('articles/', include('articles.urls')),
                  path('forum/', include('forum.urls'))
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
