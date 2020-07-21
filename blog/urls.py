from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import blog, index, post, search, filterbycat, filterbytag, save, savedlist
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog, name='post_list'),
    path('search/', search, name='search'),
    path('filterby/catagory/<str:query>', filterbycat, name='filterbycat'),
    path('filterby/tag/<str:query>', filterbytag, name='filterbytag'),
    path('tinymce/', include('tinymce.urls')),
    path('post/<slug:slug>', post, name='post_detail'),
    path('accounts/', include('allauth.urls')),
    path('save/<id>', save, name='save'),
    path('bookmarks/', savedlist, name='savedpost')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
