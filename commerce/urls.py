from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [path("admin/", admin.site.urls), path("", include("auctions.urls"))]

if settings.DEBUG and not settings.S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
