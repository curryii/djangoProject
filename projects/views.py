import json
from django.db.models import Q, QuerySet, Count, Avg, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .models import Projects
from interfaces.models import Interfaces
# Create your views here.
from django.views import View
from django.db import connection
from rest_framework import filters
from .serializers import ProjectSerializer, ProjectModelSerializer, ProjectModelSerializer_a, \
    ProjectNamesModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
import logging
from rest_framework import permissions

"""
class ListCreateAPIView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericAPIView):
    获取所以项目信息
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    创建项目信息
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""

"""
a.直接继承Mixin拓展类，拓展类只提供了action方法
b.action方法有哪些呢?
    list --> 获取列表数据
    retrieve --> 获取详情数据
    create --> 创建数据
    update --> 更新数据（完整)
    partial_update --> 更新数据（部分)
    destroy --> 删除数据
c.类视图往往只能识别如下方法?
    get --> list
    get --> retrieve
    post --> create
    put --> update
    patch --> partial_update
    delete --> destroy
d.为了进一步优化代码，需要使用具体的通用视图 XXXAPIView
"""

"""
    class ProjectView(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "^name", "=leader"]
    pagination_class = PageNumberPagination
    ordering_fields = ["id", "name", "leader"]



    获取所以项目信息
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    创建项目信息
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
GenericAPIView



    class ProjectViewId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    lookup_url_kwarg = "id"



    获取所以单笔项目信息
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    更新项目信息
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    删除项目信息
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



a.可以继承视图集父类ViewSet
b.在定义url路由条目时，支持给as_view传递字典参数（请求方法名与具体调用的action方法名的一一对应关系
c. ViewSet继承了ViewSetMixin, views.APIView
d.具备APIView的所有功能
e.继事ViewSetMixin,所有具备持给as_view传递字典参数（请求方法名与具体调用的action方法名的一一对应关系



class ProjectViewSet(
mixins.ListModelMixin,
mixins.RetrieveModelMixin,
mixins.CreateModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet):
"""

"""
定义视图集
a.ModelViewSet是一个最完整的视图集类
b.提供了获取列表数据接口、获取详情数据接口、创建数据接口、更新数据接口、删除数据接口
c.如果需要多某个模型进行增删改查操作，才会选择ModelViewSet
d.如果仅仅只对某个模型进行数据读取操作（取列表数据接口、获取详情数据接口), 一般会选择ReadOnlyModelViewSet
"""

logger = logging.getLogger("project")


class ProjectViewSet(viewsets.ModelViewSet):
    """
    list:
    获取项目列表数据

    """
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    lookup_url_kwarg = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "^name", "=leader"]
    pagination_class = PageNumberPagination
    ordering_fields = ["id", "name", "leader"]
    """
    在继承了APIView的类视图中，可以使用permission_classes类属性指定权限类,值为列表，可添加多个权限类
    
    """
    permissions_classes = [permissions.IsAuthenticated]

    """
    在继承了APIView的类视图中，可以使用authentication_classes类属性指定认证类，值为列表,可添加多个认证类
    优先级高于全局，一般无需在特定类视图中指定

    """

    """
    1、如果需要使用路由器机制自动生成路由条目，那么就必须得使用action装饰器
    2、 methods指定需要使用的请求方法, 如果不指定，默认为GET
    3、 detail指定是否为详情接口，是否需要传递当前模型的pk值[如果需要传递当前模型的pk值，那么detail=True，否则detail=False]
    4、url_path指定url路径，默认为action方法名称
    5、url_name指定url路由条目名称后缀，默认为action方法名称
    """

    """@action(methods=["GET"], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        names_list = [{"id": project.id, "name": project.name} for project in queryset]
        return Response(names_list, status=200)"""

    @action(methods=["GET"], detail=False)
    def names(self, request, *args, **kwargs):
        """queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)"""
        return super().list(request, *args, **kwargs)

    @action(methods=["GET"], detail=True)
    def interfaces(self, request, *args, **kwargs):
        project = self.get_object()
        interfaces_qs = project.inter.all()
        interfaces_list = [{"id": interfaces.id, "name": interfaces.name} for interfaces in interfaces_qs]
        logger.info(interfaces_list)
        return Response(interfaces_list, status=200)

    def get_serializer_class(self):
        """
        a.可以重写父类的get_serializer_class方法，用于为不同的action提供不一样的序列化器类
        b.在视图集对象中可以使用action属性获取当前访问的action方法名称
        """
        if self.action == "names":
            return ProjectNamesModelSerializer
        else:
            return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data.pop("create_time")
        response.data.pop("update_time")
        return response

    # 过滤
    """def filter_queryset(self, queryset):
        if self.action == "names":
            return self.queryset
        else:
            return super().filter_queryset(queryset)"""

    # 分页
    def paginate_queryset(self, queryset):
        if self.action == "names":
            return
        else:
            return super().paginate_queryset(queryset)

    def get_queryset(self):
        if self.action == "names":
            return self.queryset.filter(name__icontains="py")
        else:
            return super().get_queryset()


"""
如何定义类视图?类视图的设计原则?
a.类视图尽量要简化
b.根据需求选择相应的父类视图
c.如果DRF中的类视图有提供相应的逻辑，那么就直接使用父类提供的
d.如果DRF中的类视图，绝大多数逻辑都能满足需求，可以重写父类实现
e.如果DRF中的类视图完全不满足要求，那么就直接自定义即可
"""
