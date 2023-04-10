"""djangoProject URL Configuration

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
from rest_framework.documentation import include_docs_urls
import rest_framework_jwt.views
from projects import views
import rest_framework_jwt.settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

"""# 导入 simplejwt 提供的几个验证视图类
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)"""

schema_view = get_schema_view(
    openapi.Info(
        title="接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="文档描述",
        terms_of_service='',
        contact=openapi.Contact(email="###@qq.com"),
        license=openapi.License(name="BSD LICENSE")
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('projects.urls')),
    path('', include('interfaces.urls')),
    path('', include('users.urls')),

    path("docs/", include_docs_urls(title="测试平台接口文档", description="接口文档")),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/', include('rest_framework.urls')),

    path('user/login/', rest_framework_jwt.views.obtain_jwt_token),

]

"""# 获取Token的接口
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),"""

"""
path('api/', include('rest_framework.urls'))
在全局路由表中添加rest_framework.urls子路由
a.rest_framework. urls提供了登录和登出功能（返回的是一个HTML页面，并不是接口，)
"""
