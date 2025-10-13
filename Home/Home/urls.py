# Home/urls.py
from django.contrib import admin
from django.urls import path, include

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
