"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.urls import re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='TikTok API',
        description='...',
        default_version='v1',
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_account/', include('apps.user_account.urls')),
    path('social_login/', include(('apps.social_login.urls', 'apps.social_login'), namespace="social_login")),
    path('docs/', schema_view.with_ui('swagger')),
    path('video/', include('apps.video.urls')),
    path('chat/', include('apps.chat.urls')),
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
