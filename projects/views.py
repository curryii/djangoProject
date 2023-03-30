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
from .serializers import ProjectSerializer, ProjectModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

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
"""

"""
    获取所以项目信息
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    创建项目信息
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""

"""
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
GenericAPIView
"""

"""
    class ProjectViewId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    lookup_url_kwarg = "id"
"""

"""
    获取所以单笔项目信息
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    更新项目信息
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    删除项目信息
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

"""
a.可以继承视图集父类ViewSet
b.在定义url路由条目时，支持给as_view传递字典参数（请求方法名与具体调用的action方法名的一一对应关系
c. ViewSet继承了ViewSetMixin, views.APIView
d.具备APIView的所有功能
e.继事ViewSetMixin,所有具备持给as_view传递字典参数（请求方法名与具体调用的action方法名的一一对应关系
"""

"""
class ProjectViewSet(
mixins.ListModelMixin,
mixins.RetrieveModelMixin,
mixins.CreateModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet):
"""

"""定义视图集"""


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    lookup_url_kwarg = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "^name", "=leader"]
    pagination_class = PageNumberPagination
    ordering_fields = ["id", "name", "leader"]

    """def list(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass"""
