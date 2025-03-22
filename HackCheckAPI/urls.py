"""
URL configuration for HackCheckAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from api.views import custom_404_view
from .views import custom_media_serve


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("api.urls")),
    ]
    + [
        re_path(
            f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.+.py)$',
            custom_media_serve,
        )
    ]
    + [
        re_path(r".*", custom_404_view),
    ]
)
