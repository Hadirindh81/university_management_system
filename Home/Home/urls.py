# Home/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings               #  import settings
from django.conf.urls.static import static     #  import static for media files

urlpatterns = [
    path('admin/', admin.site.urls),

    # django auth built-ins (login/logout/password)
    path('accounts/', include('django.contrib.auth.urls')),

    # our accounts app (register/profile)
    path('accounts/', include('accounts.urls')),

    # core app
    path('', include('core.urls')),

    # fees app
    path('fees/', include('fees.urls')),
]

#  This enables serving uploaded images (media files) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
