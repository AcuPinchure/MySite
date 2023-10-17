"""MySite URL Configuration

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('local_auth.urls')),
    path('main/',include('main.urls')),
    path('bot/',include('twitter_bot.urls')),
    path('logistics/',include('logistics.urls')),
    #path('.well-known/pki-validation/<str:file_name>/',views.sslValidation) # SSL validation
    #re_path(r'',RedirectView.as_view(url='bot/index/'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
