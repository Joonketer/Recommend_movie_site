"""final_pjt_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    # 영화 관련
    path('api/v1/', include('movies.urls')),
    # 프로필,팔로우 관련
    path('profile/', include('accounts.urls')),
    # 커뮤니티 관련
    path('api/v1/community/', include('boards.urls')),
    # 계정 관련
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/user/', include('dj_rest_auth.urls')),
    # 회원가입 관련
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
