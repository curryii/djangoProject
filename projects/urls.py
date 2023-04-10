from django.urls import path, include
from projects import views
from rest_framework import routers

"""
定义类视图路由
path('project/', ProjectView.as_view())
"""

"""path('project/', ProjectView.as_view()),
    path('project/<int:id>/', ProjectViewId.as_view()),"""

"""
1、可以使用路由器对象，为视图集类自动生成路由条目
2、路由器对象默认只为通用action (create、list、retrieve、update、destroy)生成路由条目，自定义的action不会生成路由条目
3、创建SimpleRouter路由对象
4、使用路由器对象调用register方法进行注册
5、prefix指定路由前缀
6、view_set指定视图集类，不可调用as_view
"""

"""
DefaultRouter与SimpleRouter功能类似,仅有的区别为:DefaultRouter会自动生成一个根路由(显示获取数据的入口)

"""
router = routers.SimpleRouter()
# router = routers.DefaultRouter()
router.register(r"project", views.ProjectViewSet)

"""
7、加载路由条目
方式一:
路由器对象.urls属性可获取生成的路由条目path(’'， include (router. urls)),
path("", include(router.urls))
"""
urlpatterns = [


]
"""方式二:"""
urlpatterns += router.urls


"""urlpatterns = [
    path("project/", views.ProjectViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("project/<int:id>/", views.ProjectViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    })),
    path("project/names/", views.ProjectViewSet.as_view({
        "get": "names"
    })),
    path("project/<int:pk>/interfaces/", views.ProjectViewSet.as_view({
        "get": "interfaces"
    }))
]"""
